document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const usernameInput = document.querySelector("#username");
  const emailInput = document.querySelector("#email");
  const phoneInput = document.querySelector("#phone");
  const passwordInput = document.querySelector("#password");
  const confirmPasswordInput = document.querySelector("#confirm_password");

  const passwordStrengthDiv = document.querySelector("#password-strength");

  const showMessage = (input, message) => {
    const messageDiv = input.nextElementSibling;
    messageDiv.innerHTML = message;
    messageDiv.className = "message error";
  };

  const clearMessage = (input) => {
    const messageDiv = input.nextElementSibling;
    messageDiv.innerHTML = "";
    messageDiv.className = "message";
  };

  const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const isValidPhone = (phone) => /^\+?1?\d{9,15}$/.test(phone);

  usernameInput.addEventListener("input", () => {
    const value = usernameInput.value.trim();
    if (value.length < 3) {
      showMessage(
        usernameInput,
        "Input should be minimum of three characters.",
      );
    } else {
      clearMessage(usernameInput);
    }
  });

  emailInput.addEventListener("input", () => {
    const value = emailInput.value.trim();
    if (!isValidEmail(value)) {
      showMessage(emailInput, "Enter valid email ID.");
    } else {
      clearMessage(emailInput);
    }
  });

  phoneInput.addEventListener("input", () => {
    const value = phoneInput.value.trim();
    if (!isValidPhone(value)) {
      showMessage(phoneInput, "Enter valid phone number.");
    } else {
      clearMessage(phoneInput);
    }
  });

  passwordInput.addEventListener("input", () => {
    const value = passwordInput.value;
    let score = 0;
    let strength = "";
    let color = "";
    let errors = [];

    if (value.length < 8) {
      errors.push("Password should be minimum 8 characters long.");
    } else score++;

    if (!/[A-Z]/.test(value)) {
      errors.push("Password should contain upper case character.");
    } else score++;

    if (!/[a-z]/.test(value)) {
      errors.push("Password should contain lower case character.");
    } else score++;

    if (!/[0-9]/.test(value)) {
      errors.push("Password should contain numerical character.");
    } else score++;

    if (!/[@$!%*?&]/.test(value)) {
      errors.push("Password should contain special character.");
    } else score++;

    if (errors.length > 0) {
      showMessage(passwordInput, errors.join("<br>"));
    } else {
      clearMessage(passwordInput);
    }

    switch (score) {
      case 1:
        strength = "very_weak";
        color = "#dc3545";
        break;
      case 2:
        strength = "Weak";
        color = "#ffc107";
        break;
      case 3:
        strength = "Moderate";
        color = "#17a2b8";
        break;
      case 4:
        strength = "Strong";
        color = "#28a745";
        break;
      case 5:
        strength = "Very Strong";
        color = "#20c997";
        break;
      default:
        strength = "Too Short";
        color = "#6c757d";
    }

    passwordStrengthDiv.textContent = `Strength: ${strength}`;
    passwordStrengthDiv.style.color = color;
  });

  confirmPasswordInput.addEventListener("input", () => {
    if (confirmPasswordInput.value !== passwordInput.value) {
      showMessage(confirmPasswordInput, "Passwords do not match.");
    } else clearMessage(confirmPasswordInput);
  });

  form.addEventListener("submit", (event) => {
    const errors = document.querySelectorAll(".message.error");
    if (errors.length > 0) {
      event.preventDefault();
      alert("Please fix the errors in the form before submitting.");
    }
  });
});
