import React, {Component} from 'react'
import './OutletEdit.css'
import {Link, useLocation} from 'react-router-dom'
import VolunteersService from "../Services/volunteers.service";
import logo from '../public/HeartFlow_Logo_02.png'
import AuthService from "../Services/auth.service";
import {toast, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

let branchList = []
let id

export default class OutletEdit extends Component {
	constructor(props) {
		super(props);

		this.onChangeOutlet = this.onChangeOutlet.bind(this)
		this.onChangeRep = this.onChangeRep.bind(this)
		this.onChangeEmail = this.onChangeEmail.bind(this)
		this.onChangePhone = this.onChangePhone.bind(this)
		this.onChangeAddress = this.onChangeAddress.bind(this)
		this.onChangeBranch = this.onChangeBranch.bind(this)
		this.onChangePayment = this.onChangePayment.bind(this)
		this.onChangePolicy = this.onChangePolicy.bind(this)
		this.inactive = this.inactive.bind(this)
		this.submit = this.submit.bind(this)

		this.state = {
				outlet: "",
				rep: "",
				email: "",
				phone: "",
				address: "",
				branch: "",
				payment: "",
				policy: "",
				compId: "",
				paymentList: [],
				policyList: [],
				active: true,
		}


		AuthService.getBranches(
		).then(response => {
			branchList = []
			for (let i = 0; i < response.data.length; i++) {
				branchList.push(response.data[i].name)
			}
			this.forceUpdate()
		})
		let paramString = (window.location.href).split('?')[1];
		id = paramString.split("=")[1];

		VolunteersService.getOutlet(
			localStorage.getItem("userToken"),
			id
		).then(response => {
			this.setState({
				outlet: response.data.companyName,
				rep: response.data.repName,
				email: response.data.repEmail,
				phone: response.data.phone,
				address: response.data.address,
				branch: response.data.branch,
				payment: response.data.payment_method,
				policy: response.data.policy,
				active: response.data.active
			})
		}
		)

		this.paymentList = [
			"Cash on delivery",
			"Eft on delivery",
			"Cash at later time",
			"Eft at later time"
		]

		this.policyList = [
			"One week orders",
			"One month orders",
			"Six month orders"
		]
	}

	async submit(e) {
		let form = document.getElementById("outleteditForm")
		if (form.checkValidity()) {
			await VolunteersService.editOutlet(
				localStorage.getItem("userToken"),
				this.state.outlet,
				this.state.rep,
				this.state.email,
				this.state.phone,
				this.state.address,
				this.state.branch,
				this.state.payment,
				this.state.policy,
				this.state.active,
				id
			).then(response => {
				if (response.status === 200) {
					// toast.success("Successfully edited the company details.")
					alert("Successfully edited the company details.")
				} else {
					// toast.error("Unknown database error")
					alert("Unknown database error")
				}
			})
			//RESPONSE
			form.submit()
		} else {
			form.reportValidity()
		}
	}

	onChangePolicy(e) {
		this.setState({
			policy: e.target.value
		})
	}

	onChangePayment(e) {
		this.setState({
			payment: e.target.value
		})
	}

	onChangeBranch(e) {
		this.setState({
			branch: e.target.value
		})
	}

	onChangeAddress(e) {
		this.setState({
			address: e.target.value
		})
	}

	onChangePhone(e) {
		this.setState({
			phone: e.target.value
		})
	}

	onChangeEmail(e) {
		this.setState({
			email: e.target.value
		})
	}

	onChangeRep(e) {
		const re = /^[A-Za-z\s]*$/;
		if (re.test(e.target.value) || isNaN(e.target.value)) {
			this.setState({
				rep: e.target.value
			})
		}
	}

	onChangeOutlet(e) {
		const re = /^[A-Za-z\s]*$/;
		if (re.test(e.target.value) || isNaN(e.target.value)) {
			this.setState({
				outlet: e.target.value
			})
		}
	}

	inactive() {
		if (this.state.active) {
			this.setState({
				active: false
			})
			toast.success("You have set this company as inactive!")
		} else {
			this.setState({
				active: true
			})
			toast.success("You have set this company as active again")
		}
	}


	render() {
		if (localStorage.getItem("userToken") == null) {
			window.location.href = "/loginpage"
		} else {
			return (
				<div className='OutletEdit'>

					<div className='Header'/>
					<div className='Footer'/>
					<img className='logo' src = {logo} alt="Heartflow logo"/>

					<ToastContainer />
					<div className='pnlMain'>
						<span className='BRANCH'>BRANCH</span>
						<span className='PAYMENTAGREEMENT'>PAYMENT AGREEMENT</span>
						<span className='FOLLOWUPPOLICY'>FOLLOW-UP POLICY</span>
						<span className='ADDRESS'>ADDRESS</span>
						<span className='REPRESENTATIVEEMAIL'>REPRESENTATIVE EMAIL</span>
						<span className='REPCONTACTNO'>REP. CONTACT NO.</span>
						<span className='REPRESENTATIVENAME'>REPRESENTATIVE NAME</span>
						<span className='OUTLETDETAILS'>OUTLET DETAILS</span>
						<span className='OUTLETNAME'>OUTLET NAME</span>

					<form id="outleteditForm" action="https://heartflow-support-system.herokuapp.com/volunteerhomepage">
						<input type='text' className='edtOutName' onChange={this.onChangeOutlet} value={this.state.outlet} required={true} maxLength={50}/>
						<input type='text' className='edtRepName' onChange={this.onChangeRep} required={true} value={this.state.rep} maxLength={50}/>
						<input type='email' className='edtRepEmail' onChange={this.onChangeEmail} value={this.state.email} required={true}/>
						<input type='tel' className='edtRepNr' onChange={this.onChangePhone} required={true} value={this.state.phone} pattern="[0-9]{10}"/>
						<input type='text' className='edtAddress' onChange={this.onChangeAddress} value={this.state.address} required={true}/>
						<select className='edtBranch' onChange={this.onChangeBranch} required={true} value={this.state.branch}>
							{branchList.map((branch) => {
								return <option value={branch}>{branch}</option>
							})}
						</select>
						<select className='edtPayAgree' onChange={this.onChangePayment} value={this.state.paymentMethod} required={true}>
							{this.paymentList.map((payment) => {
								return <option value={payment}>{payment}</option>
							})}
						</select>
						<select className='edtPolicy' onChange={this.onChangePolicy} value={this.state.policy} required={true}>
								{this.policyList.map((policy) => {
									return <option value={policy}>{policy}</option>
								})}
						</select>
					</form>

						<button className='btnConfirm' onClick={this.submit}>
							CONFIRM
						</button>

						<button className="btnActive" onClick={this.inactive}>
							INACTIVE
						</button>
					</div>

					<Link to='/volunteerhomepage_outlets'>
						<div className='btnBack'>BACK</div>
					</Link>


				</div>
			)
		}
	}

}