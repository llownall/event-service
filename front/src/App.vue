<template>
    <div id="app">
        <div class="container-fluid">
            <div class="d-flex justify-content-center my-3">
                <h1>Сервис событий</h1>
            </div>
            <div class="d-flex justify-content-center">
                <Login v-if="showLogin" @success-login="showLogin = false"></Login>
                <Events v-if="!showLogin"></Events>
            </div>
        </div>
    </div>
</template>

<script>
    import Login from "@/components/Login";
    import Events from "@/components/Events";

    export default {
        name: 'App',
        components: {
            Login,
            Events
        },
        data() {
            return {
                showLogin: true,
            }
        }
    }
</script>

<style>
</style>
