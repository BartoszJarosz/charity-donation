document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    var checked_categories = [];

    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            // this.$el.addEventListener("click", e => {
            //   if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
            //     this.changePage(e);
            //   }
            // });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        // changePage(e) {
        //   e.preventDefault();
        //   const page = e.target.dataset.page;
        //
        //   console.log(page);
        // }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

            // update fundation list
            update_fundations()
            update_summmary()

        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            // this.currentStep++;
            // this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    var categories = $('.category');
    categories.click(function () {

        if ($(this).is(":checked")) {
            var add = true;
            for (i = 0; i < checked_categories.length; i++) {
                if (checked_categories[i] === this.value) {
                    add = false
                }
            }
            if (add) {
                checked_categories.push(this.value)
            }
        } else if ($(this).is(":not(:checked)")) {
            var index = 0;
            for (var i = 0; i < checked_categories.length; i++) {
                if (checked_categories[i] === this.value) {
                    index = i
                }
            }
            checked_categories.splice(index, 1)
        }
    });


    function update_fundations() {
        var organizations = $("[name='organization']");
        for (var i = 0; i < organizations.length; i++) {
            var hidden = true
            var cat = $(organizations[i]).data('category').replace(/(\r\n|\n|\r)\s+/gm, "").split(',');
            cat.pop();
            for (var j = 0; j < cat.length; j++) {
                if (checked_categories.includes(cat[j])) {
                    hidden = false
                }
            }
            if (hidden) {
                $(organizations[i]).parent().parent().attr("hidden", true);
            } else {
                $(organizations[i]).parent().parent().attr("hidden", false);
            }

        }
    }

    function update_summmary() {

        $('#summary_address').text($("[name='address']").val());
        $('#summary_city').text($("[name='city']").val());
        $('#summary_postcode').text($("[name='postcode']").val());
        $('#summary_phone').text($("[name='phone']").val());
        $('#summary_date').text($("[name='date']").val());
        $('#summary_time').text($("[name='time']").val());
        $('#summary_more_info').text($("[name='more_info']").val());
        var summary_text = 'Oddajesz ' + ($("[name='bags']").val()) + ' worków ';
        for (var i = 0; i < checked_categories.length; i++) {
            summary_text += checked_categories[i] + ' '
        }
        $('#summary_stuff').text(summary_text);
        var sum_institution = 'Dla ';
        sum_institution += $("input[name='organization']:checked").next().next().find('.title').text();
        $('#summary_institution').text(sum_institution);
    }

})
;
