const ActivityForm = ({
    template: '#activity_form',
    data() {
        return {
            pp_num: null,
            activity_list: [],
            image: null,
            saved_image: null,
            report: {
                date: "",
                status: "",
                finished_goods_code: "",
                quantity: "",
                report: ""
            }

        }
    },
    delimiters: ['[[', ']]'],
    computed: {

        moment: function () {
            return moment();
        },


    },

    mounted() {

        try {
            let path_array = window.location.pathname.split("/")
            let pp_num = path_array[path_array.length - 1]
            this.pp_num = pp_num
            let self = this

            axios.get('/transaction/get/activity/' + String(this.pp_num))
                .then(function (response) {
                    // console.log(response)
                    if (response.data) {
                        self.activity_list = JSON.parse(response.data)[0]
                    }
                })
                .catch(function (error) {
                    console.log(error)
                    self.$buefy.snackbar.open({
                        duration: 4000,
                        message: "Unable to load data",
                        type: 'is-light',
                        position: 'is-top-right',
                        actionText: 'Close',
                        queue: true,
                        onAction: () => {
                            this.isActive = false;
                        }
                    })


                })
            axios.get('/transaction/get/report/' + String(this.pp_num))
                .then(function (response) {
                    console.log(response)
                    if (response.data) {
                        payload = JSON.parse(response.data)
                        self.report.status = payload['flag']
                        if (payload['date'] != null) {

                            self.report.date = payload['date']
                        }
                        else {
                            self.report.date = moment().format('YYYY-MM-DD')
                        }
                        self.report.finished_goods_code = payload['finished_goods_code']
                        self.report.quantity = payload['quantity']
                        self.report.report = payload['report']
                        self.saved_image = self.getStatic(payload['image'])
                    }
                })
                .catch(function (error) {
                    console.log(error)
                    self.$buefy.snackbar.open({
                        duration: 4000,
                        message: "Unable to load data",
                        type: 'is-light',
                        position: 'is-top-right',
                        actionText: 'Close',
                        queue: true,
                        onAction: () => {
                            this.isActive = false;
                        }
                    })


                })

        }
        catch (error) {
            console.log("Unable to load data from Endpoint" + String(error))
        }
    },
    methods: {
        formatDate(data) {
            let date = String(data).split("-")
            console.log(date[2] + '-' + date[1] + '-' + date[0].slice(2,4))
            return date[2] + '-' + date[1] + '-' + date[0].slice(2, 4)
        },
        getStatic(filedata) {
            if (filedata != null) {
                let fileSrc = String('\\static') + String(filedata).split('\static')[1]
                return fileSrc
            }
            else {
                return null
            }
        },
        checkData(e) {
            console.log("In hereh")
            e.preventDefault();
            if (this.report.status && this.image && this.report.date && this.report.finished_goods_code) {

                return true;
            }
            else {
                console.log(this.report.status, this.image, this.report.date, this.report.finished_goods_code)

                return false;
            }
        },
        saveReport() {
            if (this.report.status && this.report.date) {
                let self = this
                let formData = new FormData()
                formData.append('data', JSON.stringify(this.report))
                formData.append('image', this.image)
                axios.post('/transaction/update/' + String(this.pp_num), formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    .then(function (response) {
                        if (response.data.success) {
                            self.$buefy.snackbar.open({
                                duration: 4000,
                                message: "Data updated",
                                type: 'is-light',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })

                            window.location.href = '/reports/view'
                        }
                        else {
                            self.$buefy.snackbar.open({
                                duration: 4000,
                                message: "Something went wrong",
                                type: 'is-light',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })
                        }
                    })
            }
        },
        removeImage() {
            this.report.image = null
            this.$refs.imageUpload.removeImage();

        },

        notRow(index) {
            let self = this
            console.log(index, this.activity_list)
            let item_id = this.activity_list.task_items_act[index]
            axios.post('/transaction/update/activity/item/not/' + String(item_id.id))
                .then(function (response) {
                    if (response.data.success) {

                        self.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Activity updated",
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                        item_id.flag = "not"

                    }
                    if (response.data.message) {
                        self.$buefy.snackbar.open({
                            duration: 4000,
                            message: response.data.message,
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                    }
                })

        },
        doneRow(index) {
            let self = this
            console.log(index, this.activity_list)
            let item_id = this.activity_list.task_items_act[index]
            axios.post('/transaction/update/activity/item/' + String(item_id.id))
                .then(function (response) {
                    if (response.data.success) {

                        self.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Activity marked as <b>Done </b>!",
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                        item_id.flag = "done"

                    }
                    if (response.data.message) {
                        self.$buefy.snackbar.open({
                            duration: 4000,
                            message: response.data.message,
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                    }
                })

        },
        previous() {
            try {

                this.$router.push('/view-activity')

            }
            catch (error) {
                console.log('Unable to save data - ' + String(error))
            }
        }


    }
})