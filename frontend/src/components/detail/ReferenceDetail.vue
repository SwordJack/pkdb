<template>
    <div id="reference-detail">
        <v-card flat>
            <p>
                <span class="font-weight-black">{{ reference.title }}</span><br />
                <span class="font-weight-light" v-for="(author, index) in reference.authors" :key="index">
                    {{ author.first_name }} {{ author.last_name }},
                </span><br />
                <span class="font-italic">{{ reference.journal }}, {{reference.date}}</span>
            </p>
            <p>
                <!--
                <v-btn color="black" icon v-on:click="abstractHidden = !abstractHidden">
                    <template v-if="abstractHidden">
                        <v-icon title="Show abstract" small>far fa-plus-square</v-icon>
                    </template>
                    <template v-else>
                        <v-icon title="Hide abstract">far fa-minus-square</v-icon>
                    </template>
                </v-btn>
                -->
                <a :href="'https://www.ncbi.nlm.nih.gov/pubmed/'+reference.pmid" title="PubMed" target="_blank">PMID:{{reference.pmid }}</a>
            </p>
            <p>{{ reference.abstract }}</p>
            <!--
            <p v-if="!abstractHidden" class="text-justify">
                {{ reference.abstract }}
            </p>
            -->
            </v-card>
    </div>
</template>

<script>

    export default {
        name: "ReferenceDetail",
        props: {
            reference: {
                type: Object,
            },
            resource_url: {
                type: String
            }
        },
        data() {
            return {
                abstractHidden: true
            }
        },
        computed: {
        },
        methods: {
        }
    }
</script>

<style scoped>
.v-card{
    padding: 10px;
}
</style>