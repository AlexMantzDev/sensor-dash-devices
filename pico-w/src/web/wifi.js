const form = document.getElementById("wifi-form");
let ssid = document.getElementById("ssid");
const ssidAlt = document.getElementById("ssid-alt");
const password = document.getElementById("password");
const submitBtn = document.getElementById("submit-btn");
const baseUrl = "http://10.10.10.1";

window.addEventListener("load", updateWifiOptions);
submitBtn.addEventListener("click", onSubmit);

async function onSubmit() {
	if (ssidAlt.value.trim() !== "") ssid = ssidAlt;
	const formData = {
		ssid: ssid.value,
		password: password.value,
	};
	const response = await fetch(`${baseUrl}/wifi/config`, {
		method: "POST",
		mode: "cors",
		cache: "no-cache",
		credentials: "same-origin",
		headers: {
			"Content-Type": "Application/json",
		},
		redirect: "follow",
		referrerPolicy: "no-referrer",
		body: JSON.stringify(formData),
	});
	const resData = await response.json();
	console.log(resData);
}

async function updateWifiOptions() {
	const response = await fetch(`${baseUrl}/wifi/scan`);
	const data = await response.json();
	ssid.innerHTML = "";
	data.networks.forEach((network) => {
		if (!network.ssid || network.ssid === "") {
			return;
		}
		const option = document.createElement("option");
		option.value = network.ssid;
		option.text = `${network.ssid} (${network.bssid})`;
		ssid.appendChild(option);
	});
}
