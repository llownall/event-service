<template>
    <div class="container-fluid">
        <div class="row col-md-8 col-lg-6 d-block mx-auto">
            <b-form-input
                    id="search-title"
                    v-model="searchTitle"
                    type="text"
                    placeholder="Фильтр по заголовку"
            ></b-form-input>
            <div class="btn-group mt-2 w-100" role="group" aria-label="Basic example">
                <button type="button" class="btn btn-secondary" @click="filterDatePeriod = 'all'">
                    Все
                </button>
                <button type="button" class="btn btn-secondary" @click="filterDatePeriod = 'month'">
                    За последний месяц
                </button>
                <button type="button" class="btn btn-secondary" @click="filterDatePeriod = 'week'">
                    За последнюю неделю
                </button>
                <button type="button" class="btn btn-secondary" @click="filterDatePeriod = 'day'">
                    За последний день
                </button>
            </div>

            <div class="event d-flex justify-content-between align-items-center" v-for="event in filteredEvents"
                 :key="event.id">
                <span class="ml-3">{{ event.title }}</span>
                <b-button-group class="my-auto mr-1">
                    <b-button variant="info" @click="showModal('info', event)">Подробнее</b-button>
                    <b-button variant="warning" @click="showModal('edit', event)">Изменить</b-button>
                    <b-button variant="danger" @click="deleteEvent(event)">Удалить</b-button>
                </b-button-group>
            </div>
            <b-button @click="showModal('create')" variant="success" class="d-block mx-auto mt-2">Создать</b-button>
        </div>

        <b-modal id="create-edit-modal" :title="actionText" @ok="createOrEditEvent()">
            <b-form>
                <label>Тип события:</label>
                <b-button-group class="ml-3">
                    <b-button v-for="type in types" :key="type.id"
                              @click="form.type = type.id"
                              :pressed="form.type === type.id"
                    >{{ type.text }}
                    </b-button>
                </b-button-group>

                <b-form-group class="mt-2" id="input-group-1" label="Заголовок" label-for="input-1">
                    <b-form-input
                            id="input-1"
                            v-model="form.title"
                            type="text"
                            required
                            placeholder="Введите заголовок"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Содержимое" label-for="input-2">
                    <b-form-textarea
                            id="input-2"
                            v-model="form.body"
                            placeholder="Введите подробную информацию"
                            rows="3"
                            max-rows="6"
                            required
                    ></b-form-textarea>
                </b-form-group>

                <b-form-group class="mt-2" id="input-group-3" label="День напоминания">
                    <b-form-datepicker v-model="tempDate" placeholder="Выберите день"></b-form-datepicker>
                </b-form-group>

                <b-form-group class="mt-2" id="input-group-4" label="Время напоминания">
                    <b-form-timepicker v-model="tempTime" locale="en" placeholder="Выберите время"></b-form-timepicker>
                </b-form-group>
            </b-form>
        </b-modal>

        <b-modal id="info-modal" :title="actionText" ok-only v-if="activeEvent">
            <b-form>
                <p>Тип события: {{ getTextType(activeEvent.type) }}</p>
                <p>Заголовок: {{ activeEvent.title }}</p>
                <p>Содержимое: {{ activeEvent.body }}</p>
                <p>Дата: {{ new Date(activeEvent.date).toString() }}</p>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Events',
        data() {
            return {
                events: [],
                activeEvent: undefined,
                action: '',
                actionText: '',
                searchTitle: '',
                filterDatePeriod: '',
                types: [
                    {
                        id: 0,
                        text: 'Встреча'
                    },
                    {
                        id: 1,
                        text: 'Звонок'
                    },
                ],
                form: {
                    type: 0,
                    title: '',
                    body: '',
                    date: '',
                },
                tempDate: '',
                tempTime: '',
            }
        },
        computed: {
            filteredEvents: function () {
                let filtered = this.events.filter(event => event.title.includes(this.searchTitle))
                if (this.filterDatePeriod === 'month') {
                    return filtered.filter(event => (new Date() - new Date(event.date)) < 1000 * 60 * 60 * 24 * 31)
                } else if (this.filterDatePeriod === 'week') {
                    return filtered.filter(event => (new Date() - new Date(event.date)) < 1000 * 60 * 60 * 24 * 7)
                } else if (this.filterDatePeriod === 'day') {
                    return filtered.filter(event => (new Date() - new Date(event.date)) < 1000 * 60 * 60 * 24)
                } else {
                    return filtered
                }
            }
        },
        methods: {
            getTextType(number) {
                return this.types.find(type => (type.id === number)).text;
            },
            reloadEvents() {
                let self = this
                axios.get(`http://localhost:8000/api/events/`, {
                    headers: {
                        'Authorization': `Token ${this.$store.state.token}`
                    }
                })
                    .then(function (response) {
                        console.log(response.data)
                        self.events = response.data
                        if (self.events.length > 0) {
                            self.activeEvent = self.events[0]
                        }
                    })
                    .catch(function (error) {
                        alert(error);
                    });
            },
            formClear() {
                this.form = {
                    type: 0,
                    title: '',
                    body: '',
                    date: '',
                }
            },
            showModal(action, event) {
                this.formClear()
                this.action = action
                if (action === 'create') {
                    this.actionText = 'Создать событие'
                    this.$bvModal.show('create-edit-modal')
                } else if (action === 'info') {
                    this.activeEvent = event
                    this.actionText = 'Просмотреть событие'
                    this.$bvModal.show('info-modal')
                } else if (action === 'edit') {
                    this.activeEvent = event
                    this.actionText = 'Редактировать событие'
                    this.$bvModal.show('create-edit-modal')
                    this.form = this.activeEvent
                    const eventDate = new Date(this.activeEvent.date)
                    this.tempDate = eventDate.toISOString().substring(0, 10);
                    this.tempTime = eventDate.toTimeString().substring(0, 8)
                    console.log(this.activeEvent.date)
                    console.log(eventDate.toISOString())
                    console.log(this.tempTime)
                }
            },
            createOrEditEvent() {
                let self = this
                const date = new Date(`${this.tempDate}T${this.tempTime}`)
                this.form.date = new Date(date.getTime() - new Date().getTimezoneOffset()).toISOString()
                if (this.action === 'create') {
                    axios.post(`http://localhost:8000/api/events/`, this.form, {
                        headers: {
                            'Authorization': `Token ${this.$store.state.token}`
                        }
                    })
                        .then(function (response) {
                            console.log(response)
                            self.reloadEvents()
                        })
                        .catch(function (error) {
                            alert(error);
                        });
                } else if (this.action === 'edit') {
                    axios.put(`http://localhost:8000/api/events/${this.activeEvent.id}/`, this.form, {
                        headers: {
                            'Authorization': `Token ${this.$store.state.token}`
                        }
                    })
                        .then(function (response) {
                            console.log(response)
                            self.reloadEvents()
                        })
                        .catch(function (error) {
                            alert(error);
                        });
                }
            },
            deleteEvent(item) {
                let self = this
                axios.delete(`http://localhost:8000/api/events/${item.id}/`, {
                    headers: {
                        'Authorization': `Token ${this.$store.state.token}`
                    }
                })
                    .then(function (response) {
                        console.log(response)
                        self.reloadEvents()
                    })
                    .catch(function (error) {
                        alert(error);
                    });
            },
        },
        mounted() {
            this.reloadEvents();
        }
    }
</script>

<style scoped>
    .event {
        margin: 1rem 0;
        background-color: #eaeaea;
        height: 3rem;
        border-radius: 5px;
    }
</style>
