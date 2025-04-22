document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("add-choice").addEventListener("click", function () {
    const formsetContainer = document.getElementById("formset-container");
    const totalForms = document.getElementById("id_choices-TOTAL_FORMS");
    const currentFormCount = parseInt(totalForms.value);
    const newForm = formsetContainer
      .querySelector(".formset-form:last-of-type")
      .cloneNode(true);

    // เคลียร์ค่าเดิม
    const input = newForm.querySelectorAll("input");
    input.forEach((input) => {
      if (input.name.includes("id")) {
        input.value = "";
      } else if (input.type === 'text') {
        input.value = "";
      }
    });
    
    const regex = new RegExp(`-${currentFormCount - 1}-`, "g");
    input.innerHTML = newForm.innerHTML.replace(
      regex,
      `-${currentFormCount}-`
    );

    formsetContainer.appendChild(newForm);
    totalForms.value = currentFormCount + 1;
  });
});
