import React, { Component, useState } from 'react'
import './DirectorHomePage_Outlets.css'
import ImgAsset from '../public'
import { Link } from 'react-router-dom'
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { Button, rgbToHex } from "@material-ui/core";
import AuthService from "../Services/auth.service";
import { useEffect } from 'react';
import VolunteersService from "../Services/volunteers.service";


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
];

export default function DirectorHomePage_Outlets() {

    const [dataGridRows, setDataGridRows] = React.useState([]);
    const [directorName, setDirectorName] = React.useState("Charl Reyneke");



    useEffect(() => {
        AuthService.getInfo(localStorage.getItem("userToken")
        ).then(response => {
            setDirectorName(response.data['first_name'] + " " + response.data['last_name'])
        })
    }, [])

    function openNav() {
		document.getElementById("mySidenav").style.width = "250px";
	}

	function closeNav() {
  		document.getElementById("mySidenav").style.width = "0";
	}

    function admin() {
        window.location.href = "https://heartflow-support-system.herokuapp.com/admin"
    }

    useEffect(() => {
        VolunteersService.getOutlets(
            localStorage.getItem("userToken")
        ).then(response => {
            setDataGridRows(dataGridRows => [])
            for (let i = 0; i < response.data['length']; i++) {
                setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'],  company :response.data[i]['companyName'], paymentMethod: response.data[i]['payment_method'], uptodate: response.data[i]['upToDate'] , repName: response.data[i]['repName'], email: response.data[i]['repEmail'], phone: response.data[i]['phone'], policy: response.data[i]['policy'], address: response.data[i]['address']}])
            }
        })
    }, [])

    if (localStorage.getItem("userToken") == null) {
        window.location.href = "/loginpage"
    } else {
        return (
            <div>
                <div id="mySidenav" className="sidenav">
					<a href="javascript:void(0)" className="closebtn" onClick={closeNav}>&times;</a>
                    <a href="https://heartflow-support-system.herokuapp.com/directorhomepage">Volunteers</a>
					<a href="https://heartflow-support-system.herokuapp.com/directorhomepage_coupons">Online Coupons</a>
					<a href="https://heartflow-support-system.herokuapp.com/directorhomepage_Deliveries">Deliveries</a>
					<a href="https://heartflow-support-system.herokuapp.com/directorhomepage_outlets">Outlets</a>
				</div>
                <div className='DirectorHomePage_Outlets'>

                    <div className='Header' />
                    <div className='Footer' />

                    <Link to='/directorhomemenu'>
                        <div className='btnOptions' />
                    </Link>

                    <Button className='adminPortal' onClick={admin}>ADMIN PORTAL</Button>

                    <Link to='/'>
                        <Button className='btnLogout'>LOG OUT</Button>
                    </Link>

                    <Link to='/editdirectorpage'>
                        <Button className='btnEditProfile'>EDIT PROFILE</Button>
                    </Link>

                    <span className='NAMEOFDIRECTOR'> {directorName} </span>


                    <div style={{ height: 450, width: '1100px' }}>
                        <DataGrid
                            rows={dataGridRows}
                            columns={columns}
                            pageSize={5}
                            rowsPerPageOptions={[5]}
                            sx={{
                                top: '200px',
								left: '40%',
                                height: '600px',
                                width: '1400px',
								color: 'rgb(0, 0, 0)',
								fontFamily: 'Montserrat',
								fontSize: '20px',
								fontWeight: '500',
								justifyContent: 'left',
								textAlign: 'left',
								borderRadius: '40px',
								backgroundColor: 'rgb(220, 220, 220)',
								opacity: '0.98',
                            }} />

                    </div>
                    <button className="btnNavbar" onClick={openNav}>
						NAVIGATION
				</button>
                </div>
            </div>
        )
    }


}
