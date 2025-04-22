document.addEventListener("DOMContentLoaded", function () {
  let questionCount = 1;

  document
    .getElementById("add-question-btn")
    .addEventListener("click", function () {
      const container = document.getElementById("questions-container");
      const questionBlock = document
        .querySelector(".question-block")
        .cloneNode(true);

      // Clear ค่าที่กรอกไว้
      questionBlock.querySelector('input[name="questions[]"]').value = "";
      questionBlock.querySelector('select[name="types[]"]').value = "choice";

      const choicesSection = questionBlock.querySelector(".choices-section");
      const choiceList = choicesSection.querySelector(".choice-list");
      choiceList.innerHTML = `
      <div class="input-group mb-1">
        <input type="text" name="choices_${questionCount}[]" class="form-control" placeholder="ตัวเลือกที่ 1" />
        <button type="button" class="btn btn-outline-danger remove-choice-btn">ลบ</button>
      </div>
      <div class="input-group mb-1">
        <input type="text" name="choices_${questionCount}[]" class="form-control" placeholder="ตัวเลือกที่ 2" />
        <button type="button" class="btn btn-outline-danger remove-choice-btn">ลบ</button>
      </div>
    `;

      container.appendChild(questionBlock);
      questionCount++;
    });

  document.addEventListener("click", function (e) {
    // เพิ่มตัวเลือก
    if (e.target.classList.contains("add-choice-btn")) {
      const choiceSection = e.target.closest(".choices-section");
      const questionBlock = e.target.closest(".question-block");
      const index = [...document.querySelectorAll(".question-block")].indexOf(
        questionBlock
      );
      const newInput = document.createElement("div");
      newInput.classList.add("input-group", "mb-1");
      newInput.innerHTML = `
        <input type="text" name="choices_${index}[]" class="form-control" placeholder="ตัวเลือกที่เพิ่มเติม" />
        <button type="button" class="btn btn-outline-danger remove-choice-btn">ลบ</button>
      `;
      choiceSection.querySelector(".choice-list").appendChild(newInput);
    }
    // เพิ่มตัวเลือก 5-1 อัตโนมัติ
    if (e.target.classList.contains("insert-default-btn")) {
      const block = e.target.closest(".question-block");
      const index = [...document.querySelectorAll(".question-block")].indexOf(
        block
      )
      const choiceList = block.querySelector(".choice-list");
      choiceList.innerHTML = ""; // ล้างก่อน
      
      [5, 4, 3, 2, 1].forEach((score) => {
        const input = document.createElement("div");
        input.classList.add("input-group", "mb-1");
        input.innerHTML = `
          <input type="text" name="choices_${index}[]" class="form-control" value="${score}" />
          <button type="button" class="btn btn-outline-danger remove-choice-btn">ลบ</button>
        `;
        choiceList.appendChild(input);
      });
    }

    // ลบตัวเลือก
    if (e.target.classList.contains("remove-choice-btn")) {
      const group = e.target.closest(".input-group");
      if (group.parentNode.children.length > 1) {
        group.remove();
      } else {
        alert("ต้องมีตัวเลือกอย่างน้อย 1 ตัว");
      }
    }

    // ลบคำถาม
    if (e.target.classList.contains("remove-question-btn")) {
      const block = e.target.closest(".question-block");
      const allBlocks = document.querySelectorAll(".question-block");
      if (allBlocks.length > 1) {
        block.remove();
      } else {
        alert("ต้องมีคำถามอย่างน้อย 1 ข้อ");
      }
    }

    // ซ่อน/แสดงตัวเลือกตามประเภทคำถาม
    if (e.target.classList.contains("question-type-select")) {
      const questionBlock = e.target.closest(".question-block");
      const choicesSection = questionBlock.querySelector(".choices-section");
      choicesSection.style.display =
        e.target.value === "choice" ? "block" : "none";
    }
  });
});
