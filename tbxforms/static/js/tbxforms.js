import '../sass/tbxforms.scss';

class TbxForms {
    static selector() {
        return 'form.tbxforms-form';
    }

    constructor(node) {
        this.form = node;

        // Loop through all elements within the given form (e.g. inputs, divs, fieldsets).
        this.form.querySelectorAll('*').forEach((formElement) => {
            // If this element has conditional logic...
            if (
                formElement.dataset.conditionalFieldName &&
                formElement.dataset.conditionalFieldValues
            ) {
                const container = formElement.closest('.tbxforms-form-group')
                    ? formElement.closest('.tbxforms-form-group')
                    : formElement;
                const drivingFieldNodeList = document.querySelectorAll(
                    `${this.form} [name="${formElement.dataset.conditionalFieldName}"]`,
                );
                let conditionalValuesForElement;

                // Try to parse the JSON containing required field mapping.
                try {
                    conditionalValuesForElement = JSON.parse(
                        formElement.dataset.conditionalFieldValues,
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
                                conditionalValuesForElement.includes(
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

                        // Trigger above event listener to correct presentation.
                        option_node.dispatchEvent(new Event('change'));
                    });
                } else {
                    // We're dealing with a single field.

                    const drivingField = drivingFieldNodeList.item(0);

                    drivingField.addEventListener('change', () => {
                        if (
                            conditionalValuesForElement.includes(
                                drivingField.value,
                            ) ||
                            conditionalValuesForElement.includes(
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

                    // Trigger above event listener to correct presentation.
                    drivingField.dispatchEvent(new Event('change'));
                }
            }
        });

        // Clear any values for fields that are conditionally hidden.
        // NB. We don't use `this.form.elements.('[hidden=true]')` to include divs.
        this.form.addEventListener('submit', () => {
            this.form
                .querySelectorAll('[hidden=true]')
                .forEach((hiddenFormElement) => {
                    this.clearInput(hiddenFormElement);
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
            // case 'select': // Requires different logic (see below).
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
            // If this is a container element run again for child elements.
            // NB. maybe a `default` case would be better here.
            case 'div':
            case 'fieldset':
                node.querySelectorAll('*').forEach((formElement) => {
                    this.clearInput(formElement);
                });
                break;
        }
    }
}

export default TbxForms;
