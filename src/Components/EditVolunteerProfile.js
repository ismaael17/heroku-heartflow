import React, {Component} from 'react'
import './EditVolunteerProfile.css'
import {Link} from 'react-router-dom'
import VolunteersService from "../Services/volunteers.service";
import {Button} from "@material-ui/core";
import emblem from '../public/HF_emblem.png'
import AuthService from "../Services/auth.service";
import {toast, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';


let branchList = []
export default class EditVolunteerProfile extends Component {

	constructor(props) {
		super(props);

		this.onChangeName = this.onChangeName.bind(this)
		this.onChangeSurname = this.onChangeSurname.bind(this)
		this.onChangeBranch = this.onChangeBranch.bind(this)
		this.onChangeNumber = this.onChangeNumber.bind(this)
		this.submit = this.submit.bind(this)
		this.info = this.info.bind(this)
		this.info_email = this.info_email.bind(this)

		this.state = {
			name: "",
			surname: "",
			email: "",
			branch: "",
			number: "",
		}
		AuthService.getBranches(
		).then(response => {
			branchList = []
			for (let i = 0; i < response.data.length; i++) {
				branchList.push(response.data[i].name)
			}
			this.forceUpdate()
		})


		VolunteersService.getVolunteerDetails(
			localStorage.getItem("userToken")
		).then(response => {
			if (response.status === 200) {
				console.log(response.data)
				this.setState({
					name: response.data["first_name"],
					surname: response.data["last_name"],
					email: response.data["email"],
					branch: response.data["branch"],
					number: response.data["phone"]
				})
			}
		})

	}

	info() {
		toast.info("Please contact a director to change your branch.")
	}

	info_email() {
		toast.info("Please create a new account or contact a director.")
	}

	async submit(e) {
		let form = document.getElementById("editVolunteerDetails")

		if (form.checkValidity()) {
			await VolunteersService.editVolunteerProfile(
				localStorage.getItem("userToken"),
				this.state.name,
				this.state.surname,
				this.state.branch,
				this.state.number
			).then(response => {
				if (response.status === 200) {
					// toast.success("Successfully changed your details")
					alert("Successfully changed your details")
				} else if (response.status === 404) {
					// toast.error("Details could not be updated")
					alert("Details could not be updated")
				}
			})
			//RESPONSE
			form.submit()
		} else {
			form.reportValidity()
		}

	}

	onChangeName(e) {
		const re = /^[A-Za-z\s]*$/;
		if (re.test(e.target.value) || isNaN(e.target.value.charCodeAt(0))) {
			this.setState({
				name: e.target.value
			});
		}
	}

	onChangeSurname(e) {
		const re = /^[A-Za-z\s]*$/;
		if (re.test(e.target.value) || isNaN(e.target.value.charCodeAt(0))) {
			this.setState({
				surname: e.target.value
			});
		}
	}

	onChangeNumber(e) {
		this.setState({
			number: e.target.value
		})
	}


	onChangeBranch(e) {
		this.setState({
			branch: e.target.value
		})
	}

	render() {
		return (
			<div className='EditVolunteerProfile_EditVolunteerProfile'>

				<div className='Header'/>
				<div className='Footer'/>
				<span className='EDITPROFILE'>EDIT PROFILE</span>
				<img className='emblem' src = {emblem}/>
				<ToastContainer />
				<div className='pnlMain' >

					<span className='NAME'>NAME</span>
					<span className='BRANCH'>BRANCH</span>
					<span className='NUMBER'>PHONE NUMBER</span>
					<span className='EMAIL'>EMAIL</span>
					<span className='SURNAME'>SURNAME</span>

					<form id='editVolunteerDetails' action="http://localhost:3000/volunteerhomepage">
						<input type='text' className='edtName' onChange={this.onChangeName} value={this.state.name} required={true} />
						<input type='text' className='edtSurname' onChange={this.onChangeSurname} value={this.state.surname} required={true} />
						<input type='text' className='edtEmail' value={this.state.email} onClick={this.info_email} readOnly={true} />
						<input type='text' className='edtBranch' onChange={this.onChangeBranch} onClick={this.info} value={this.state.branch} readOnly={true} />
						<input type='tel' className='edtNumber' onChange={this.onChangeNumber} value={this.state.number} required={true} pattern="[0-9]{10}" />
					</form>

					<Button className='btnConfirm' onClick={this.submit}>CONFIRM</Button>

					<Link to={{ pathname: "https://heartflow-support-system.herokuapp.com/reset_password" }} target="_blank">
						<Button className='btnForgot'>
							Forgot Password?
						</Button>
					</Link>
				</div>

				<Link to='/volunteerhomepage'>
					<Button className='btnBack'>BACK</Button>
				</Link>


			</div>
		)
	}
}