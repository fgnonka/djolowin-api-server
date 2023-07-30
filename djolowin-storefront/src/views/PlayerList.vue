<template>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h1 class="white-text">Players</h1>
                <hr class="bg-white">
            </div>
            <div class="row" v-for="player in allPlayers" :key="player.id">
                <div class="col-md-4">
                    <div class="card rounded card-template hover14 border-secondary m-4">
                        <div class="card-header border-0 bg-transparent">
                            <div class="card-container">
                                <h6>
                                    <div class="">
                                        <h4 class="">{{ player.name }}</h4>
                                    </div>
                                    <div class="d-flex justify-content-center">
                                        <h4 class="">
                                            {{ player.jerseyNumber }}
                                            <br />
                                            {{ player.dateOfBirth }}
                                            <br />
                                            {{ player.team.country.country }}
                                        </h4>
                                    </div>
                                    <div class="">
                                        <h4 class="">#{{ player.position }}</h4>
                                    </div>
                                </h6>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import gql from "graphql-tag";

export default {
    name: "PlayerList",
    data() {
        return {
            allPlayers: [],
        };
    },
    async created() {
        const players = await this.$apollo.query({
            query: gql`
                query {
                    allPlayers {
                        id
                        name
                        dateOfBirth
                        jerseyNumber
                        slug
                        position
                        team{
                            country{
                            country
                            }
                        }
                    }
                }
            `,
        });
        this.allPlayers = players.data.allPlayers;
    }
}
</script>