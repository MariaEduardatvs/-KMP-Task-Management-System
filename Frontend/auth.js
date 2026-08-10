// REGISTER

const registerForm = document.getElementById("registerForm");

if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;

    const password = document.getElementById("password").value;

    const response = await fetch(
      "/register",

      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          username,

          password,
        }),
      },
    );

    const result = await response.json();

    alert(result.message);
  });
}

// LOGIN

const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("loginUsername").value;

    const password = document.getElementById("loginPassword").value;

    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    const result = await response.json();

    // If login was successful, go to the task page
    if (response.ok) {
      window.location.href = "/tasks";
    }
  });
}
