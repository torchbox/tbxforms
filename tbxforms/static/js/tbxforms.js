import '../sass/tbxforms.scss';

/**
 * Updates the visibility of a form element based on conditional field values
 * @param {HTMLElement} container - The container element to show/hide
 * @param {NodeList} drivingFieldNodeList - List of form fields that control visibility
 * @param {Array} conditionalValuesForElement - Values that should trigger showing the container
 */
function updateVisibility(
  container,
  drivingFieldNodeList,
  conditionalValuesForElement
) {
  let shouldShow = false;

  if (drivingFieldNodeList.length > 1) {
    // For checkboxes/radios, check if any are checked with matching values
    drivingFieldNodeList.forEach(function (field) {
      if (field.checked && conditionalValuesForElement.includes(field.value)) {
        shouldShow = true;
      }
    });
  } else {
    // For single fields, check the value directly
    const field = drivingFieldNodeList.item(0);
    shouldShow =
      conditionalValuesForElement.includes(field.value) ||
      conditionalValuesForElement.includes(Number(field.value));
  }

  // Update visibility and aria states
  container.hidden = !shouldShow;
  drivingFieldNodeList.forEach((field) =>
    field.setAttribute('aria-expanded', shouldShow.toString())
  );
}

/**
 * Initializes form functionality with conditional field visibility
 * @param {HTMLFormElement} form - The form element to initialize
 * @constructor
 */
function TbxForms(form) {
  this.form = form; // Stash the TbxForms DOM element.
  const self = this; // Stash the TbxForms instance.

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

      try {
        conditionalValuesForElement = JSON.parse(
          formElement.dataset.conditionalFieldValues
        );
      } catch (e) {
        throw 'Invalid JSON: ' + e;
      }

      container.classList.add('tbxforms-conditional');

      // Set up change listeners
      drivingFieldNodeList.forEach(function (field) {
        field.addEventListener('change', function () {
          updateVisibility(
            container,
            drivingFieldNodeList,
            conditionalValuesForElement
          );
        });
      });

      // Check initial state
      updateVisibility(
        container,
        drivingFieldNodeList,
        conditionalValuesForElement
      );
    }
  });

  // Clear any values for fields that are conditionally hidden.
  // NB. We don't use `form.elements.('[hidden]')` to include divs.
  form.addEventListener('submit', function () {
    form.querySelectorAll('[hidden]').forEach(function (hiddenFormElement) {
      self.clearInput(hiddenFormElement);
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
          console.debug(
            `Skipping unsupported node.type '${node.type}' while trying to clearInput().`
          );
      }
      break;

    case 'TEXTAREA':
      node.value = '';
      break;

    case 'SELECT':
      node.selectedIndex = -1;
      break;

    // If this is a container element, run again for child elements.
    case 'DIV':
    case 'FIELDSET':
      node.querySelectorAll('*').forEach(function (formElement) {
        self.clearInput(formElement);
      });
      break;

    default:
      console.debug(
        `Skipping unsupported node.tagName '${node.tagName}' while trying to clearInput().`
      );
  }
};

TbxForms.selector = function () {
  return 'form.tbxforms';
};

export default TbxForms;
