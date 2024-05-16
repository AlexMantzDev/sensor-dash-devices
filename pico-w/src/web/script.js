const form = document.getElementById("form");

function onSubmit() {
	const formData = new FormData(form);
	const data = Object.fromEntries(formData);
	console.log(data);
	fetch("/api/v1/submit", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	})
		.then((response) => response.json())
		.then((data) => {
			console.log("Success:", data);
			form.reset();
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}
