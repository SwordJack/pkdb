<template>
<span>
    <v-tabs
            v-model="active"
            color="#999999"
            dark
            slider-color="yellow">
        <v-tab
                v-for="(item, i) in files"
                :key="i"
                ripple
        >
            {{ id_from_name(item.name) }}
        </v-tab>
        <v-tab-item v-for="item in files" :key="item.name">
            <v-card flat>
                <get-file :resource_url="backend+item.file">
                    <template slot-scope="data">
                        <v-img :src="data.data"
                               max-height="500"
                               max-width="500"
                               :alt="item.name"
                               :contain="true"
                               @click="next"
                        />
                    </template>

                </get-file>

            </v-card>
        </v-tab-item>
    </v-tabs>

    </span>
</template>

<script>
    /**
     * Displaying files from the database.
     */
    import {UrlMixin} from "../tables/mixins";
    import GetFile from "../api/GetFile";

    export default {
        name: "FileImageView",
        components: {
            GetFile
        },
        props: {
            files: {
                type: Array,
                required: true,
            }
        },
        mixins:[UrlMixin],
        data () {
            return {
                active: null,
            }
        },
        computed: {
            backend(){
                    return this.$store.state.django_domain;
                },
            images() {
                var list = [];
                for (var k=0; k<this.files.length; k++){
                    var item = this.files[k];
                    if (item.name.endsWith("png")){
                        list.push(item)
                    }
                }
                return list.sort(function(a, b){
                    return a.name.localeCompare(b.name)
                });

            }
        },
        methods: {
            id_from_name: function (name) {
                let tokens = name.split("_");
                let id = tokens[tokens.length-1];
                id = id.split(".")[0];
                return id
            },
            next () {
                const active = parseInt(this.active);
                this.active = (active < (this.images.length-1) ? active + 1 : 0)
            }
        }
    }
</script>

<style scoped>
    .v-card {
        padding: 10px;
    }
</style>