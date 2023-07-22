<template>
  <q-page class="row items-start justify-center top-content" padding>
    <div class="column" style="width: 100%; max-width: 1200px">
      <!-- Add this wrapper div -->
      <!-- Display the text search mode message -->
      <div class="hero q-mt-md">
        <div class="q-mb-md">
          Empower Your Tweets<br />Custom Comment Generation Tailored for You!
        </div>
      </div>
      <q-form style="width: 100%; max-width: 1200px" class="">
        <div class="row">
          <q-input
            outlined
            v-model="tweetUrl"
            label="Enter Tweet URL . . ."
            style="width: 100%; max-width: 1600px"
            type="url"
            class="col"
          >
            <!-- <template v-slot:append> </template>
          <template v-slot> </template> -->
          </q-input>
          <q-btn-dropdown :label="mood" color="black" outline no-caps>
            <q-list>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section>
                  <q-item-label>Positive</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section>
                  <q-item-label>Nuetral</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section>
                  <q-item-label>Negative</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
          <q-input
            class="col"
            v-model.number="num"
            min="1"
            type="number"
            outlined
            style="max-width: 200px"
          />
        </div>
        <div class="text-center">
          <q-btn
            no-caps
            color="primary"
            style="height: 55px; width: 40%"
            class="text-primary q-my-md"
            icon-right="chevron_right"
            :label="`Generate Tweets for $${cost.toFixed(2)}`"
            @click="generateTweets(tweetUrl, mood, num)"
          />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import axios from "axios";

export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      tweetUrl: "",
      num: 1,
      mood: "Positive",
    };
  },
  methods: {
    onItemClick(event) {
      this.mood = event.target.innerText;
    },
    calculateCost() {
      const costPerComment =
        this.mood === "Positive" ? 0.4 : this.mood === "Negative" ? 0.8 : 0.6;
      return costPerComment * this.num;
    },
    generateTweets(tweetUrl, mood, num) {
      axios
        .post("http://10.0.0.128:5000/tweet_process", {
          tweet_url: tweetUrl,
          mood: mood,
          num: num,
        })
        .then((response) => {
          console.log(response.data);
          // Here you can handle the response from the Flask application.
        })
        .catch((error) => {
          console.error(error);
          // Here you can handle the error if the request fails.
        });
    },
  },
  computed: {
    cost() {
      return this.calculateCost();
    },
  },
});
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap");

.center {
  margin-left: auto;
  margin-right: auto;
}
.hero {
  font-size: 2.5rem;
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: -0.02em;
  text-align: center;
  color: #263238;
  margin-bottom: 1.5rem;
  font-family: "Roboto", sans-serif;
}
</style>
