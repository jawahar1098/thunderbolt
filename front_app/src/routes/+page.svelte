<script>
	// @ts-nocheck
	
	  
	import '../global.css'
	import { goto } from '$app/navigation';
	import {basepath} from "$lib/config";
	export let userDetails;

	import { userDetailsStore } from '$lib/datastore.js';
	import { style } from 'd3';
	
	
	
	  let email = "";
	  let resetemail = ''
	  let newpass = ''
	  let errorMessage = '';
	  let password1 = "";
	  let showProgress = false;


	async function requestResetPassword() {
		const response = await fetch(basepath()+'/reset-password-notify', {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ email })
		});
		const result = await response.json();

		if (response.ok) {
			alert('Reset password request sent successfully.');
		} else {
			alert('Failed to send reset password request.');
		}
	}



	  async function login() {
		if (
	  
		  email === '' ||
		  password1 === ''
		
		) {
		  alert('Please fill in all the required fields.');
		  return;
		}
		console.log(email)
		const response = await fetch(basepath()+'/loginapi', {
		  method: "POST",
		  headers: {
			"Content-Type": "application/json"
		  },
		  body: JSON.stringify({ email, password1 })
		});
		const u_data = await response.json()
		if (!response.ok) {
		  const userDetails = u_data.userdata;
		  if (userDetails.message.includes('Email')) {
			  errorMessage = userDetails.message;
			//   showProgress = false;
			  alert(errorMessage)
			} else if (userDetails.message.includes('password1')) {
				errorMessage = userDetails.message;
			alert(errorMessage)
		  } else {
			// showProgress = true;
			errorMessage = userDetails.message;
			alert(errorMessage)
		  }
		}
		
		if (u_data.message === 'success' ) {
			showProgress = true;

			console.log("show progress:",showProgress)

		 const userDetails = u_data.userdata;
		 userDetailsStore.set(userDetails);
		  console.log(userDetails, "designationssss");
		  console.log(userDetails.designation, "designation");
		  console.log(userDetails.officername,"officerdata");
		  console.log(userDetails.email,"email");
		  console.log(userDetails.availability,"availability");
		  console.log(userDetails.team,"team");
		  console.log(userDetails.modules,"modules");
		  console.log(userDetails.superior,"superior");
		  console.log(userDetails.all,"all");
		  localStorage.setItem("userAuth", true);
		  localStorage.setItem("jwt", `Bearer ${u_data.access_token}`);
		  localStorage.setItem("userDetails",JSON.stringify(userDetails));
		  console.log(localStorage.getItem("userAuth"), "login localauth");
		  console.log(userDetails, userDetails.role)
	
		  if(
			userDetails.role === "Analyst"              || 
			userDetails.designation === "DSP"           || 
			userDetails.designation === "SI"            || 
			userDetails.designation === "SP"            ||
			userDetails.role === "Logger"               || 
			userDetails.role === "Mailer"               || 
			userDetails.designation === "INSPR"         ||
			userDetails.designation === "ADDL-SP/DSP"   ||
			userDetails.designation === "IG"            ||
			userDetails.designation === "DIG"
		  ){
			goto('/dashboard', { state: { userDetails } });     
		  }
		  else if(userDetails.designation === "Administrator"){
			goto('/ticketing/superadmin/');
		  }
		   
		} else {
		  alert("Invalid User or User is already Logged IN");
		}
	  }
	
	</script>
  <main>
	<div class="center-container">
		<div class="header-container">
			<h1 class="heading">THUNDER<i class="bi bi-lightning-charge-fill"></i>BOLT</h1>
		</div>
		<div class="login-container">
			<div class="login-title">LOGIN</div>
			<form class="inputs">
				<label>Username</label>
				<input type="text" placeholder="Enter your username" bind:value={email}>
				<label>Password</label>
				<input type="password" placeholder="Enter your password" bind:value={password1}>
				<button class="btn-login" on:click={login}>Login</button>
			</form>
			<a class="forget" href="!#">Forgot Password</a>
		</div>
		<img src="/modified.png" alt="Watermark" class="watermark">
		<!-- <div class="img">
			<img src="/modified.png" alt="logo">
		</div> -->
		<div class="footer-container">
			<h2 class="footer">SPECIAL INTELLIGENCE BRANCH</h2>
			<h3 style="color: black;">Andhra Pradesh</h3>
		</div>
	</div>
	{#if showProgress}
	<div class="position-absolute top-50 start-50 translate-middle p-5">
		<div class="spinner-border text-primary" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
	{/if}
</main>

<style>
	main {
		background: #adb5bd;  /* fallback for old browsers */
		background: -webkit-linear-gradient(to right, #ffffff, #ab98d1);  /* Chrome 10-25, Safari 5.1-6 */
		background: linear-gradient(to right, #96b8b993, #dbd4e7); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

		/* background-color: orange; */
		/* background: linear-gradient(to bottom, #c0b444, #c5b208); */
		/* background-image: url('/'); */
		height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center;
		font-family: 'Open Sans', sans-serif;
		overflow: hidden;
		opacity: 1;
		
	}

	.center-container {
		width: 900px;
		text-align: center;
		color: #ebe2e2;
		opacity: 1;
		z-index: 1;
	}

	.header-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-bottom: 80px;
	}
	.header-image {
		width: 70px;
		height: 70px;
		margin-left: 20px; 
		margin-bottom: 50px;
	}

	.heading {
		font-family: Georgia, 'Times New Roman', Times, serif;
		font-size: 5rem;
		font-weight: bolder;
		margin: 20px 0;
		color: black;
		margin-top: -40px;
	}

	.footer-container {
		margin-top: 90px;
	}
	.footer {
		font-family: Georgia, 'Times New Roman', Times, serif;
		font-size: 3rem;
		font-weight: bold;
		margin: 20px 0;
		color: black;
	}
	.login-container {
		padding: 20px;
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
		border-radius: 8px;
		width: 500px;
		margin-left: 23%;
		/* background-color: #a3afca; */
		/* background-image: url('/modified.png'); */
	}
	/* .img {
		margin-top: 20px;
		display: block; 
		margin-left: auto;
		margin-right: auto;
	} */

	.login-title {
		font-size: 22px;
		font-weight: bold;
		margin-bottom: 30px;
		color: black;
	}

	.inputs label {
		display: block;
		margin-bottom: 5px;
		color: black;
	}

	.inputs {
		text-align: left;
		margin-bottom: 25px;
	}

	input[type="text"], input[type="password"] {
		width: calc(100% - 20px);
		padding: 10px;
		margin-bottom: 20px;
		border: 1px solid #72879b;
		border-radius: 5px;
		/* background-color: #b0c3d6; */
		background: transparent;
		color: #1a1818;
	}

	.btn-login {
		width: calc(100% - 20px);
		padding: 10px;
		border: none;
		border-radius: 5px;
		background-color: #e9af59;
		color: #272424;
		cursor: pointer;
		margin-top: 20px;
	}

	.forget {
		display: block;
		margin-top: 20px;
		color: #ebe2e2;
	}
	.watermark {
		position: absolute;
		/* bottom: 0; 
		right: 0; */
		top: 45%;
		left: 50%;
		transform: translate(-50%, -50%);
		opacity: 0.1; 
		z-index: -1;
		max-width: 100%;
		height: auto;
	}

</style>
