import '../sass/tbxforms.scss';

class TbxForms {
    static selector() {
        return 'form.tbxforms-form';
    }

    constructor(node) {
        this.form = node;

        // Loop through all elements within the given form (e.g. inputs, divs, fieldsets).
        this.form.querySelectorAll('*').forEach((form_element) => {
            // If this element has conditional logic...
            if (
                form_element.dataset.conditionalFieldName &&
                form_element.dataset.conditionalFieldValues
            ) {
                const container = form_element.closest('.tbxforms-form-group')
                    ? form_element.closest('.tbxforms-form-group')
                    : form_element;
                const drivingFieldNodeList = document.querySelectorAll(
                    `${this.form} [name="${form_element.dataset.conditionalFieldName}"]`,
                );

                // Try to parse the JSON and log an error if there's a problem.
                try {
                    const conditional_values_for_element = JSON.parse(
                        form_element.dataset.conditionalFieldValues,
                    );
                } catch (e) {
                    throw 'Invalid JSON: ' + e;
                }

                container.classList.add('tbxforms-conditional');

                if (drivingFieldNodeList.length > 1) {
                    // We're dealing with radios or checkboxes.
                    drivingFieldNodeList.forEach((option_node) => {
                        option_node.addEventListener('change', () => {
                            if (
                                option_node.checked &&
                                conditional_values_for_element.includes(
                                    option_node.value,
                                )
                            ) {
                                option_node.setAttribute(
                                    'aria-expanded',
                                    'true',
                                );
                                container.hidden = false;
                            } else {
                                option_node.setAttribute(
                                    'aria-expanded',
                                    'false',
                                );
                                container.hidden = true;
                            }
                        });

                        // Trigger the event listener.
                        option_node.dispatchEvent(new Event('change'));
                    });
                } else {
                    // We're dealing with a single field.
                    const drivingField = drivingFieldNodeList.item(0);

                    drivingField.addEventListener('change', () => {
                        if (
                            conditional_values_for_element.includes(
                                drivingField.value,
                            ) ||
                            conditional_values_for_element.includes(
                                Number(drivingField.value),
                            )
                        ) {
                            drivingField.setAttribute('aria-expanded', 'true');
                            container.hidden = false;
                        } else {
                            drivingField.setAttribute('aria-expanded', 'false');
                            container.hidden = true;
                        }
                    });

                    // Trigger the event listener.
                    drivingField.dispatchEvent(new Event('change'));
                }
            }
        });

        // Clear any values for fields that are conditionally hidden.
        // NB. We don't use `this.form.elements.('[hidden=true]')` to include divs.
        this.form.addEventListener('submit', () => {
            this.form
                .querySelectorAll('[hidden=true]')
                .forEach((hidden_form_element) => {
                    this.clearInput(hidden_form_element);
                });
        });
    }

    clearInput(node) {
        /*
            Reset the value of a given input, or if we're given a container
            (e.g. div, fieldset, etc.) then reset the fields within the container
            instead.
        */
        switch (node.type) {
            // Taken from https://www.w3schools.com/html/html_form_input_types.asp
            case 'button':
            case 'checkbox':
            case 'color':
            case 'date':
            case 'datetime-local':
            case 'email':
            case 'file':
            case 'hidden':
            case 'image':
            case 'month':
            case 'number':
            case 'password':
            case 'radio':
            case 'range':
            case 'reset':
            case 'search':
            case 'submit':
            case 'tel':
            case 'text':
            case 'textarea':
            case 'time':
            case 'url':
            case 'week':
                node.value = '';
                break;
            case 'select':
                node.selectedIndex = -1;
                break;
            default:
                node.querySelectorAll('*').forEach((form_element) => {
                    this.clearInput(form_element);
                });
        }
    }
}

export default TbxForms;