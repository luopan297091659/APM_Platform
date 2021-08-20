    <template>
    <div class="timer">
    <div ref="startTimer"></div>
    </div>
    </template>
    <script>
        export default {
            name: 'Timer',
            data () {
            return {
            timer: "",
            content: "",
            hour: 0,
            minutes: 0,
            seconds: 0
            }
        },
        created () {
            this.timer = setInterval(this.startTimer, 1000);
        },
        destroyed () {
            clearInterval(this.timer);
        },

        methods: {
            startTimer () {
            this.seconds += 1;
            if (this.seconds >= 60) {
            this.seconds = 0;
            this.minute = this.minute + 1;
        }

        if (this.minute >= 60) {
        this.minute = 0;
        this.hour = this.hour + 1;
        }
        this.$refs.startTimer.innerHTML = (this.minutes < 10 ? '0' + this.minutes : this.minutes) + ':' + (this.seconds < 10 ? '0' + this.seconds : this.seconds);
        }
        }
        }
    </script>
    <style>
    </style>
