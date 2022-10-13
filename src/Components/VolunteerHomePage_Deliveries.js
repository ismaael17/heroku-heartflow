import React, {Component, useEffect} from 'react'
import './VolunteerHomePage_Deliveries.css'
import {Link} from 'react-router-dom'
import {Container} from '../Container'
import VolunteersService from "../Services/volunteers.service";
import {DataGrid, GridColDef, GridValueGetterParams} from "@mui/x-data-grid";
import logo from '../public/HeartFlow_Logo_02.png'
import emblem from '../public/HF_emblem.png'
import igLogo from '../public/ig_logo.png'
import fbLogo from '../public/fb_logo.png'

var globalNewSelection

let status = [
	"Paid",
	"Not Paid"
]
const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'company', headerName: 'Company', width: 150 },
  { field: 'paymentMethod', headerName: 'Payment Method', width: 150 },
  { field: 'amount', headerName: 'No. of Coupons', width: 180 },
  { field: 'paid', headerName: 'Paid', width: 100 },
  { field: 'date', headerName: 'Date', width: 300 },
  { field: 'comments', headerName: 'Comment', width: 180 },
];

function logout() {
	localStorage.removeItem("userToken")
	localStorage.removeItem("Volunteer")
}


export default function VolunteerHomePage_Deliveries() {

	const [select_status, setStatus] = React.useState(["None"]);
	const [table_status, setTable] = React.useState(["All"]);
	const [dataGridRows, setDataGridRows] = React.useState([]);
	const [select, setSelection] = React.useState([]);


	function changeTable() {
		VolunteersService.getDeliveries(
			localStorage.getItem("userToken"),
			table_status
		).then(response => {
			setDataGridRows(dataGridRows => [])
			for (let i = 0; i < response.data['length']; i++) {
				//Edit this data here
                setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'],  company :response.data[i]['company'], paymentMethod: response.data[i]['paymentMethod'], amount: response.data[i]['amount'], paid:response.data[i]['paid'], date: response.data[i]['date'], comments: response.data[i]['comments']}])
            }
		})
	}


	async function handleSubmit() {
		console.log(select_status)
		await VolunteersService.changeStatus(
			localStorage.getItem("userToken"),
			select_status,
			globalNewSelection[0]
		).then(response => {
		})
		window.location.reload(false);
	}

	async function changePaid() {
		//THOMAS DIE IS NET VIR JOU
		if (select_status[0] !== "None") {
			await VolunteersService.changePaid(
				localStorage.getItem("userToken"),
				select_status,
				globalNewSelection[0]
			).then(response => {
				alert("Succesfull change")
			})
			window.location.reload(false);
		} else {
			alert("Please change to 'Not Paid' or 'Paid' for the order!")
		}
	}

	function openNav() {
		document.getElementById("mySidenav").style.width = "250px";
	}

	function closeNav() {
  		document.getElementById("mySidenav").style.width = "0";
	}

	useEffect(() => {
		VolunteersService.getDeliveries(
			localStorage.getItem("userToken"),
			"All"
		).then(response => {
			setDataGridRows(dataGridRows => [])
			for (let i = 0; i < response.data['length']; i++) {
				//Edit this data here
                setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'],  company :response.data[i]['company'], paymentMethod: response.data[i]['payment_method'], amount: response.data[i]['amount'], paid:response.data[i]['paid'], date: response.data[i]['date'], comments: response.data[i]['comments']}])
            }
		})
	}, [])


	//checking if the user is logged in
	if (localStorage.getItem("userToken") == null) {
		window.location.href = "/loginpage"
	} else {
		return (
			<div>
				<div id="mySidenav" className="sidenav">
					<a href="javascript:void(0)" className="closebtn" onClick={closeNav}>&times;</a>
					<a href="https://heartflow-support-system.herokuapp.com/volunteerhomepage">Online Coupons</a>
					<a href="https://heartflow-support-system.herokuapp.com/volunteerhomepage_Deliveries">Deliveries</a>
					<a href="https://heartflow-support-system.herokuapp.com/volunteerhomepage_outlets">Outlets</a>
				</div>
				<div className='VolunteerHomePage_Deliveries'>
					<div className='Header'/>
					<div className='Footer'/>
					<img className='logo' src = {logo}/>
					<img className='emblem' src = {emblem}/>
					<div className='Footer'>
						<span className='CONTACT'>CONTACT US</span>
						<Link to={{ pathname: "https://www.instagram.com/heartflow_npc/" }} target="_blank">
							<img className='IG_logo' src = {igLogo}/>
						</Link>
						<Link to={{ pathname: "https://www.facebook.com/HeartFlowHomeless/" }} target="_blank">
							<img className='FB_logo' src = {fbLogo}/>
						</Link>
					</div>

					<div style={{ height: 700, width: '50%' }}>
						<DataGrid
							rows={dataGridRows}
							columns={columns}
							pageSize={11}
							rowsPerPageOptions={[5]}
							onSelectionModelChange={async (newSelection) => {
								setSelection(newSelection.selectionModel)
								globalNewSelection = newSelection
								await VolunteersService.getDeliveryDetails(
									localStorage.getItem("userToken"),
									globalNewSelection[0]
								).then(response => {
									document.getElementById("form_status").disabled = false
								})
							}}
							sx={{	top: '191px',
								left: '50%',
								color: 'rgb(0, 0, 0)',
								fontFamily: 'Montserrat',
								fontSize: '20px',
								fontWeight: '500',
								justifyContent: 'left',
								textAlign: 'left',
								borderRadius: '40px',
								backgroundColor: 'rgb(220, 220, 220)',
								opacity: '0.98',
							 }}/>
					</div>

					<div className='pnlMain'>
						<span className='ACTIONS'>ACTIONS</span>
						<Link to='/volunteerpickuppage'>
							<button className='btnPickUp'>PICK UP</button>
						</Link>
						<Link to='/volunteerexchange'>
							<div className='btnExchange'>EXCHANGE</div>
						</Link>
						<Link to='/volunteerdelivery'>
							<div className='btnDelivery'>DELIVERY</div>
						</Link>
						<Link to='/volunteerdiscardloss'>
							<div className='btnLoss'>LOSS/DISCARD</div>
						</Link>
						<Link to='/outletregistration'>
							<div className='btnRegister'>REGISTER</div>
						</Link>
					</div>

					<Link to='/'>
						<button className='btnLogOut' onClick={logout}>
							LOG OUT
						</button>
					</Link>

					<Link to='/editvolunteerprofile'>
						<button className='btnEditProf' >
							EDIT PROFILE
						</button>
					</Link>

					<div className='pnlTable'>
					<span className='TABLE'>TABLE</span>
					<select className='status' onChange={event => setTable(event.target.value)} onClick={changeTable} defaultValue={"All"}>
						<option value="All">All</option>
						{status.map((status) => { return <option value={status}>{status}</option> })}
					</select>

					<select className='form_status' id="form_status" onChange={event => setStatus(event.target.value)} disabled={true}>
							{status.map((status) => { return <option value={status}>{status}</option> })}
							<option value="" disabled selected hidden>Change Paid</option>
					</select>

					<button className="popupButton" onClick={changePaid}>
						UPDATE PAID
					</button>

					<button className="btnNavbar" onClick={openNav}>
						NAVIGATION
					</button>
				</div>
			</div>

			</div>
		)
	}

}
