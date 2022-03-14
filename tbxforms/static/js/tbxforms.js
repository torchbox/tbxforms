import '../sass/tbxforms.scss';

/**
 * CustomEvent polyfill for IE11.
 * https://stackoverflow.com/a/26596324/1798491
 */
(function () {
  if (typeof window.CustomEvent === 'function') return false; //If not IE

  function CustomEvent(event, params) {
    params = params || { bubbles: false, cancelable: false, detail: undefined };
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent(
      event,
      params.bubbles,
      params.cancelable,
      params.detail
    );
    return evt;
  }

  CustomEvent.prototype = window.Event.prototype;

  window.CustomEvent = CustomEvent;
})();

function TbxForms(form) {
  this.form = form;

  // Loop through all elements within the given form (e.g. inputs, divs, fieldsets).
  form.querySelectorAll('*').forEach(function (formElement) {
    // If this element has conditional logic...
    if (
      formElement.dataset.conditionalFieldName &&
      formElement.dataset.conditionalFieldValues
    ) {
      const container = formElement.closest('.tbxforms-form-group')
        ? formElement.closest('.tbxforms-form-group')
        : formElement;
      const drivingFieldNodeList = form.querySelectorAll(
        '[name="' + formElement.dataset.conditionalFieldName + '"]'
      );
      let conditionalValuesForElement;

      // Try to parse the JSON containing required field mapping.
      try {
        conditionalValuesForElement = JSON.parse(
          formElement.dataset.conditionalFieldValues
        );
      } catch (e) {
        throw 'Invalid JSON: ' + e;
      }

      container.classList.add('tbxforms-conditional');

      if (drivingFieldNodeList.length > 1) {
        // We're dealing with radios or checkboxes.

        drivingFieldNodeList.forEach(function (option_node) {
          option_node.addEventListener('change', function () {
            if (
              option_node.checked &&
              conditionalValuesForElement.includes(option_node.value)
            ) {
              option_node.setAttribute('aria-expanded', 'true');
              container.hidden = false;
            } else {
              option_node.setAttribute('aria-expanded', 'false');
              container.hidden = true;
            }
          });

          // Trigger above event listener to correct presentation.
          option_node.dispatchEvent(new CustomEvent('change'));
        });
      } else {
        // We're dealing with a single field.

        const drivingField = drivingFieldNodeList.item(0);

        drivingField.addEventListener('change', function () {
          if (
            conditionalValuesForElement.includes(drivingField.value) ||
            conditionalValuesForElement.includes(Number(drivingField.value))
          ) {
            drivingField.setAttribute('aria-expanded', 'true');
            container.hidden = false;
          } else {
            drivingField.setAttribute('aria-expanded', 'false');
            container.hidden = true;
          }
        });

        // Trigger above event listener to correct presentation.
        drivingField.dispatchEvent(new CustomEvent('change'));
      }
    }
  });

  // Clear any values for fields that are conditionally hidden.
  // NB. We don't use `form.elements.('[hidden]')` to include divs.
  form.addEventListener('submit', function () {
    form.querySelectorAll('[hidden]').forEach(function (hiddenFormElement) {
      form.clearInput(hiddenFormElement);
    });
  });
}

/**
 * Reset the value of a given input, or if we're given a container
 * (e.g. div, fieldset, etc.) then reset the fields within the container
 * instead.
 */
TbxForms.prototype.clearInput = function (node) {
  const self = this;

  switch (node.tagName) {
    case 'INPUT':
      switch (node.type) {
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
        case 'range':
        case 'reset':
        case 'search':
        case 'tel':
        case 'text':
        case 'time':
        case 'url':
        case 'week':
          node.value = '';
          break;

        case 'radio':
        case 'checkbox':
          node.checked = false;
          break;

        default:
          console.error(
            "Unexpected node.type '" +
              node.type +
              "' found while trying to clearInput."
          );
      }
      break;

    case 'TEXTAREA':
      node.value = '';
      break;

    case 'SELECT':
      node.selectedIndex = -1;
      break;

    // If this is a container element run again for child elements.
    // NB. maybe a `default` case would be better here.
    case 'DIV':
    case 'FIELDSET':
      node.querySelectorAll('*').forEach(function (formElement) {
        self.clearInput(formElement);
      });
      break;

    default:
      console.error(
        "Unexpected node.tagName '" +
          node.tagName +
          "' found while trying to clearInput."
      );
  }
};

TbxForms.selector = function () {
  return 'form.tbxforms';
};

export default TbxForms;
