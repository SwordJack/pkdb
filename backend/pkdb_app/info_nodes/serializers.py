from rest_framework import serializers

from pkdb_app import utils
from pkdb_app.info_nodes.documents import InfoNodeDocument
from pkdb_app.info_nodes.models import InfoNode, Synonym, Annotation, Unit, MeasurementType, Substance, Choice, Route, \
    Form, Tissue, Application
from pkdb_app.serializers import WrongKeyValidationSerializer, ExSerializer
from pkdb_app.utils import update_or_create_multiple


class EXMeasurementTypeableSerializer(ExSerializer):
    measurement_type = serializers.CharField(allow_blank=False)
    measurement_type_map = serializers.CharField(allow_blank=False)


class MeasurementTypeableSerializer(EXMeasurementTypeableSerializer):
    substance = utils.SlugRelatedField(
        slug_field="name",
        queryset=InfoNode.objects.filter(ntype=InfoNode.NTypes.Substance),
        read_only=False,
        required=False,
        allow_null=True,
    )

    measurement_type = utils.SlugRelatedField(
        slug_field="name",
        queryset=InfoNode.objects.filter(ntype=InfoNode.NTypes.MeasurementType)
    )

    choice = serializers.CharField(allow_null=True)


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep


class SynonymSerializer(WrongKeyValidationSerializer):
    pk = serializers.IntegerField(read_only=True)
    class Meta:
        model = Synonym
        fields = ["name","pk"]

    def to_internal_value(self, data):
        return {"name": data}


class AnnotationSerializer(serializers.ModelSerializer):
    term = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    label = serializers.CharField(allow_null=True)

    class Meta:
        model = Annotation
        fields = ["term", "relation", "collection", "description", "label"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["name"]

    def to_internal_value(self, data):
        return {"name": data}

    def to_representation(self, instance):
        return instance.name


class SubstanceExtraSerializer(serializers.ModelSerializer):
    derived = serializers.BooleanField(read_only=True)

    class Meta:
        model = Substance
        fields = ["mass", "charge", "formula", "derived"]


class MeasurementTypeExtraSerializer(serializers.ModelSerializer):
    choices = serializers.SlugRelatedField("name", many=True, read_only=True)
    units = UnitSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = MeasurementType
        fields = ["units", "choices"]


class ChoiceExtraSerializer(serializers.ModelSerializer):
    measurement_types = serializers.SlugRelatedField("sid", many=True, queryset=InfoNode.objects.filter(
        ntype=InfoNode.NTypes.MeasurementType), required=False, allow_null=True)

    class Meta:
        model = Choice
        fields = ["measurement_types"]


class InfoNodeSerializer(serializers.ModelSerializer):
    """ Substance. """
    parents = utils.SlugRelatedField(many=True, slug_field="sid", queryset=InfoNode.objects.all(),
                                     required=False, allow_null=True)
    synonyms = SynonymSerializer(many=True, read_only=False, required=False, allow_null=True)
    annotations = AnnotationSerializer(many=True, read_only=False, required=False, allow_null=True)
    measurement_type = MeasurementTypeExtraSerializer(allow_null=True, required=False)
    substance = SubstanceExtraSerializer(allow_null=True, required=False)
    choice = ChoiceExtraSerializer(allow_null=True, required=False)

    class Meta:
        model = InfoNode
        fields = ["sid", "url_slug", "name", "ntype", "dtype", "parents", "description", "synonyms", "creator",
                  "annotations", "measurement_type", "substance", "choice"]

    @staticmethod
    def NTypes():
        return {
            "info_node": InfoNode,
            "measurement_type": MeasurementType,
            "substance": Substance,
            "route": Route,
            "form": Form,
            "application": Application,
            "tissue": Tissue,
            "choice": Choice,
        }

    def update_or_create(self, validated_data, instance=None):
        synonyms_data = validated_data.pop("synonyms", [])
        parents_data = validated_data.pop("parents", [])
        annotations_data = validated_data.pop("annotations", [])
        ntype = validated_data.get('ntype')
        extra_fields = validated_data.pop(ntype, {})
        Model = self.NTypes()[ntype]

        if instance is None:
            instance = InfoNode.objects.create(**validated_data)

        update_or_create_multiple(instance, annotations_data, 'annotations', lookup_fields=["term", "relation"])
        update_or_create_multiple(instance, synonyms_data, 'synonyms', lookup_fields=["name"])
        instance.parents.clear()
        instance.parents.add(*parents_data)
        instance.save()

        if Model != InfoNode:
            if Model == MeasurementType:
                units = extra_fields.pop('units', [])
                specific_instance, _ = Model.objects.update_or_create(info_node=instance, defaults=extra_fields)
                update_or_create_multiple(specific_instance, units, 'units', lookup_fields=["name"])

            elif Model == Choice:
                measurement_types = extra_fields.pop('measurement_types', [])
                specific_instance, _ = Model.objects.update_or_create(info_node=instance, defaults=extra_fields)
                specific_instance.measurement_types.clear()
                specific_instance.measurement_types.add(*measurement_types)
                InfoNodeDocument().update(measurement_types)

            else:
                specific_instance, _ = Model.objects.update_or_create(info_node=instance, defaults=extra_fields)

            specific_instance.save()

        InfoNodeDocument().update(instance)

        return instance

    def update(self, instance, validated_data):

        return self.update_or_create(validated_data=validated_data, instance=instance)

    def create(self, validated_data):
        return self.update_or_create(validated_data=validated_data)

    def to_internal_value(self, data):
        data["creator"] = self.context['request'].user.id
        return super().to_internal_value(data)

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data["creator"] = instance.creator.username
        return data


###############################################################################################
# Elastic Serializer
###############################################################################################


class SmallInfoNodeElasticSerializer(serializers.ModelSerializer):
    annotations = AnnotationSerializer(many=True, allow_null=True)

    class Meta:
        model = InfoNode
        fields = ["sid", "name", "description", "annotations"]


class InfoNodeElasticSerializer(serializers.ModelSerializer):
    parents = SmallInfoNodeElasticSerializer(many=True)
    annotations = AnnotationSerializer(many=True, allow_null=True)
    synonyms = SynonymSerializer(many=True, allow_null=True)
    substance = SubstanceExtraSerializer(required=False, allow_null=True)
    measurement_type = MeasurementTypeExtraSerializer(required=False, allow_null=True)

    class Meta:
        model = InfoNode
        fields = ["sid", "name", 'url_slug', "ntype", "dtype", "description", "synonyms", "parents", "annotations",
                  "measurement_type", "substance"]

