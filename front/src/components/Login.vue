<template>
    <div>
        <h3 class="text-center mb-4">Вход/регистрация</h3>
        <b-form @submit="onSubmit">
            <b-form-group id="input-group-1" label="Email:" label-for="input-1">
                <b-form-input
                        id="input-1"
                        v-model="email"
                        type="email"
                        required
                        placeholder="Введите email"
                        autocomplete="off"
                ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Пароль:" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="password"
                        type="password"
                        required
                        placeholder="Введите пароль"
                        autocomplete="off"
                ></b-form-input>
            </b-form-group>

            <b-button type="submit" variant="primary" class="mx-auto d-block">Отправить</b-button>
        </b-form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Login',
        data() {
            return {
                email: '',
                password: '',
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                let self = this
                axios.post(`http://localhost:8000/api/login/`, {
                    username: this.email,
                    password: this.password
                })
                    .then(function (response) {
                        self.$store.commit('setToken', response.data.token);
                        self.$emit('success-login')
                    })
                    .catch(function (error) {
                        alert(error);
                    });
            },
        }
    }
</script>

<style scoped>
</style>
