window.addEventListener('DOMContentLoaded', () => {
    const cls_hidden = "govuk-conditional--hidden";
    const cls_visible = "govuk-conditional--visible";

    function clearInput(node) {
        /*
            Reset the value of a given input, or if we're given a container
            (e.g. div, fieldset, etc.) then reset the fields within the container
            instead.
       */
        switch(node.type) {
            // Taken from https://www.w3schools.com/html/html_form_input_types.asp
            case "button":
            case "checkbox":
            case "color":
            case "date":
            case "datetime-local":
            case "email":
            case "file":
            case "hidden":
            case "image":
            case "month":
            case "number":
            case "password":
            case "radio":
            case "range":
            case "reset":
            case "search":
            case "submit":
            case "tel":
            case "text":
            case "textarea":
            case "time":
            case "url":
            case "week":
                node.value = ""
                break;
            case "select":
                node.selectedIndex = -1;
                break;
            default:
                node.querySelectorAll('*').forEach((child_node) =>{
                    clearInput(child_node);
                });
        }
    }

    document.querySelectorAll('form.govuk-form').forEach((form) => {
        // Loop through all elements within forms (e.g. inputs, divs, fieldsets).
        form.querySelectorAll('*').forEach((node) => {

            // If this element has conditional logic...
            if (node.dataset.conditionalFieldName && node.dataset.conditionalFieldValues) {
                const container = (node.closest(".govuk-form-group")) ? node.closest(".govuk-form-group") : node;
                const drivingFieldNodeList = document.getElementsByName(node.dataset.conditionalFieldName);

                container.classList.add("govuk-conditional");

                if (drivingFieldNodeList.length > 1) {
                    // We're dealing with radios or checkboxes.
                    drivingFieldNodeList.forEach((option_node) => {
                        option_node.addEventListener('change', () => {
                            if (option_node.checked && JSON.parse(node.dataset.conditionalFieldValues).includes(option_node.value)) {
                                option_node.setAttribute('aria-expanded', 'true');
                                container.classList.remove(cls_hidden);
                                container.classList.add(cls_visible);
                            } else {
                                option_node.setAttribute('aria-expanded', 'false');
                                container.classList.remove(cls_visible);
                                container.classList.add(cls_hidden);
                            }
                        });

                        // Trigger the event listener.
                        option_node.dispatchEvent(new Event("change"));
                    });
                } else {
                    // We're dealing with a single field.
                    const drivingField = drivingFieldNodeList.item(0);

                    drivingField.addEventListener('change', () => {
                        if (JSON.parse(node.dataset.conditionalFieldValues).includes(drivingField.value) || JSON.parse(node.dataset.conditionalFieldValues).includes(Number(drivingField.value))) {
                            drivingField.setAttribute('aria-expanded', 'true');
                            container.classList.remove(cls_hidden);
                            container.classList.add(cls_visible);
                        } else {
                            drivingField.setAttribute('aria-expanded', 'false');
                            container.classList.remove(cls_visible);
                            container.classList.add(cls_hidden);
                        }
                    });

                    // Trigger the event listener.
                    drivingField.dispatchEvent(new Event("change"));
                }
            }
        })

        // Clear any values for fields that are conditionally hidden.
        form.addEventListener('submit', () => {
            form.querySelectorAll(`.${cls_hidden}`).forEach((node) => {
                clearInput(node);
            });
        });
    })
});
