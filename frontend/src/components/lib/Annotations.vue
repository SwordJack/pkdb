<template>
    <div id="annotations">
        <v-card flat v-if="(item.comments && item.comments.length>0) || (item.descriptions && item.descriptions.length>0)">
            <descriptions v-if="item.descriptions" :descriptions="item.descriptions"/>
            <comments v-if="item.comments" :comments="item.comments"/>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: "Annotations",
        props: {
            item: {
                type: Object,
            }
        }
    }
</script>

<style scoped>

</style>