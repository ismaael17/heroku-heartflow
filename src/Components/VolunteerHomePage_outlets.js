import React, {Component, useEffect} from 'react'
import './VolunteerHomePage_outlets.css'
import {Link} from 'react-router-dom'
import VolunteersService from "../Services/volunteers.service";
import {DataGrid, GridColDef, GridValueGetterParams} from "@mui/x-data-grid";
import logo from '../public/HeartFlow_Logo_02.png'
import emblem from '../public/HF_emblem.png'
import igLogo from '../public/ig_logo.png'
import fbLogo from '../public/fb_logo.png'
import OutletRegistration from "./OutletRegistration";
import {toast, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';



var globalNewSelection

let status = [
	"Paid",
	"Not Paid"
]
const columns: GridColDef[] = [
  	{ field: 'id', headerName: 'ID', width: 70 },
  	{ field: 'company', headerName: 'Company', width: 150 },
  	{ field: 'paymentMethod', headerName: 'Payment Method', width: 150 },
	{ field: 'uptodate', headerName: 'Up to Date', width: 150 },
  	{ field: 'repName', headerName: 'Rep Name', width: 180 },
	{ field: 'email', headerName:'Rep Email', width: 200},
	{ field: 'phone', headerName: 'Phone', width: 90 },
	{ field: 'policy', headerName: 'Policy', width: 200 },
  	{ field: 'address', headerName: 'Address', width: 180 },
	{ field: 'followUp', headerName: 'Follow Up', width: 150}
];

function logout() {
	localStorage.removeItem("userToken")
	localStorage.removeItem("Volunteer")
}


export default function VolunteerHomePage_outlets() {
	const [dataGridRows, setDataGridRows] = React.useState([]);
	const [select, setSelection] = React.useState([]);

	async function changePaid() {
		//THOMAS DIE IS NET VIR JOU
		if (globalNewSelection === undefined) {
			toast.info("Please select a company to edit.")
		} else {
			window.location.href = "https://heartflow-support-system.herokuapp.com/outletedit?id=" + globalNewSelection[0];
		}
	}

	function openNav() {
		document.getElementById("mySidenav").style.width = "250px";
	}

	function closeNav() {
  		document.getElementById("mySidenav").style.width = "0";
	}

	useEffect(() => {
		VolunteersService.getOutlets(
			localStorage.getItem("userToken")
		).then(response => {
			setDataGridRows(dataGridRows => [])
			for (let i = 0; i < response.data['length']; i++) {
				//Edit this data here
                setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'],  company :response.data[i]['companyName'], paymentMethod: response.data[i]['payment_method'], uptodate: response.data[i]['upToDate'] , repName: response.data[i]['repName'], email: response.data[i]['repEmail'], phone: response.data[i]['phone'], policy: response.data[i]['policy'], address: response.data[i]['address'], followUp: response.data[i]['followUp']}])
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
				<div className='VolunteerHomePage_outlets'>
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
					<ToastContainer/>
					<div style={{ height: 700, width: '50%' }}>
						<DataGrid
							rows={dataGridRows}
							columns={columns}
							pageSize={5}
							rowsPerPageOptions={[5]}
							onSelectionModelChange={async (newSelection) => {
								setSelection(newSelection.selectionModel)
								globalNewSelection = newSelection
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

					<button className="popupButton" onClick={changePaid}>
						EDIT OUTLET
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
