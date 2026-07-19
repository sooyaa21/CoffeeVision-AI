// =====================================================
// CoffeeVision AI
// Main JavaScript
// =====================================================

document.addEventListener("DOMContentLoaded", function () {
alert("JavaScript Berjalan");

    const imageInput = document.getElementById("imageInput");
    const previewImage = document.getElementById("previewImage");
    const fileName = document.getElementById("fileName");
    const fileSize = document.getElementById("fileSize");
    const uploadStatus = document.getElementById("uploadStatus");
    const uploadArea = document.querySelector(".upload-area");
    const predictButton = document.querySelector(".predict-btn");
    const form = document.querySelector("form");

    // ============================
    // Preview Gambar
    // ============================

    if (imageInput) {

        imageInput.onchange = function () {

            if (!this.files.length) return;

            const file = this.files[0];

            // Preview
            const reader = new FileReader();

            reader.onload = function (e) {

                previewImage.src = e.target.result;
                previewImage.style.display = "block";

            }

            reader.readAsDataURL(file);

            // Nama File
            fileName.innerHTML =
                '<i class="fa-solid fa-file-image"></i> ' + file.name;

            // Ukuran File
            if (file.size > 1024 * 1024) {

                fileSize.innerHTML =
                    (file.size / 1024 / 1024).toFixed(2) + " MB";

            } else {

                fileSize.innerHTML =
                    (file.size / 1024).toFixed(2) + " KB";

            }

            // Status
            uploadStatus.innerHTML =
                "✅ Gambar berhasil dipilih dan siap dianalisis";

            uploadStatus.style.background = "#22C55E";
            uploadStatus.style.color = "#fff";
            uploadStatus.style.padding = "10px 18px";
            uploadStatus.style.borderRadius = "30px";

            uploadArea.style.borderColor = "#22C55E";

        };

    }

    // ============================
    // Drag & Drop
    // ============================

    if (uploadArea) {

        uploadArea.addEventListener("dragover", function (e) {

            e.preventDefault();

            uploadArea.style.borderColor = "#3B82F6";

        });

        uploadArea.addEventListener("dragleave", function () {

            uploadArea.style.borderColor = "#BCAAA4";

        });

        uploadArea.addEventListener("drop", function (e) {

            e.preventDefault();

            imageInput.files = e.dataTransfer.files;

            imageInput.dispatchEvent(new Event("change"));

        });

    }

    // ============================
    // Loading Button
    // ============================

    if (form) {

        form.addEventListener("submit", function () {

            predictButton.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Sedang Menganalisis...';

            predictButton.disabled = true;

        });

    }

    // ============================
    // Sidebar Active
    // ============================

    document.querySelectorAll(".menu a").forEach(link => {

        link.addEventListener("click", function () {

            document.querySelectorAll(".menu a").forEach(a => {

                a.classList.remove("active-menu");

            });

            this.classList.add("active-menu");

        });

    });

    // ============================
    // Smooth Scroll
    // ============================

    document.querySelectorAll(".menu a").forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

});