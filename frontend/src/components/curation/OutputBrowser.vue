<template>
    <span>
  <v-card dark>
    <v-card-title class="headline blue">
      {{ title }}
    </v-card-title>
    <v-card-text>
      <v-autocomplete
              v-model="model"
              :items="items"
              color="white"
              hide-no-data
              hide-selected
              item-text="Description"
              item-value="API"
              label="Pharmacokinetics types"
              placeholder="Start typing to Search"
              persistent-hint
              return-object
      ></v-autocomplete>
    </v-card-text>

    <v-divider></v-divider>
      <v-card-text v-if="description">

          <strong>Description:</strong> {{ description }}<br />
          <strong>Units:</strong> {{ units }}
      </v-card-text>

    <v-expand-transition color="blue lighten-1">

      <v-list v-if="choices.length">
          <v-card-text>Choices</v-card-text>
        <v-list-tile v-for="(field, i) in choices" :key="i">
          <v-list-tile-content>
            <v-list-tile-title v-text="field"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-expand-transition>
  </v-card>
      <!--{{ options }}-->
    </span>
</template>

<script>
    export default {
        name: "OuputBrowser",
        props: {
            options: {
                type: Object,
                required: true
            },
            title: {
                type: String,
                required: true
            }
        },
        data: () => ({
            model: null,
        }),
        computed: {
            items () {
                return Object.keys(this.options['pktypes']).sort()
            },
            choices () {
                if (!this.model) {
                    return []
                }
                // FIXME: there seems to be a bug here
                return []
            },
            description () {
              if (!this.model) {
                return null;
              }
              const data = this.options['pktypes'][this.model];
              return data['description'];
            },
            units () {
              if (!this.model) {
                return null;
              }
              const data = this.options['pktypes'][this.model];
              return data['units'];
            }

        },
    }
</script>

<style scoped>

</style>