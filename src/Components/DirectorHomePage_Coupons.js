import React, { Component, useState } from 'react'
import './DirectorHomePage_Coupons.css'
import ImgAsset from '../public'
import { Link } from 'react-router-dom'
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { Button, rgbToHex } from "@material-ui/core";
import AuthService from "../Services/auth.service";
import { useEffect } from 'react';
import VolunteersService from "../Services/volunteers.service";


const columns: GridColDef[] = [
	{ field: 'id', headerName: 'ID', width: 70 },
	{ field: 'firstName', headerName: 'First name', width: 150 },
	{ field: 'lastName', headerName: 'Last name', width: 150 },
	{ field: 'coupons', headerName: 'No. of Coupons', width: 180 },
	{ field: 'branch', headerName: 'Branch', width: 200 },
	{ field: 'paid', headerName: 'Paid (R)', width: 90 },
	{ field: 'status', headerName: 'Status', width: 180 },
];

export default function DirectorHomePage_Coupons() {

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
        VolunteersService.getOnlineOrders(
            localStorage.getItem("userToken"),
            "All"
        ).then(response => {
            setDataGridRows(dataGridRows => [])
            for (let i = 0; i < response.data['length']; i++) {
				setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'], firstName: response.data[i]['name'], lastName: response.data[i]['surname'], coupons: response.data[i]['amount'], branch: response.data[i]['branch'], paid: response.data[i]['paid'], status: response.data[i]['status'] }])
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
                    <a href="http://localhost:3000/directorhomepage">Volunteers</a>
					<a href="http://localhost:3000/directorhomepage_coupons">Online Coupons</a>
					<a href="http://localhost:3000/directorhomepage_Deliveries">Deliveries</a>
					<a href="http://localhost:3000/directorhomepage_outlets">Outlets</a>
				</div>
                <div className='DirectorHomePage_Coupons'>

                    <div className='Header' />
                    <div className='Footer' />

                    <Link to='/directorhomemenu'>
                        <div className='btnOptions' />
                    </Link>

                    <Link to='/'>
                        <Button className='btnLogout'>LOG OUT</Button>
                    </Link>

                    <Button className='adminPortal' onClick={admin}>ADMIN PORTAL</Button>

                    <Link to='/editdirectorpage'>
                        <Button className='btnEditProfile'>EDIT PROFILE</Button>
                    </Link>

                    <span className='NAMEOFDIRECTOR'> {directorName} </span>


                    <div style={{ height: 450, width: '1100px' }}>
                        <DataGrid
                            rows={dataGridRows}
                            columns={columns}
                            pageSize={9}
                            rowsPerPageOptions={[5]}
                            sx={{
                                top: '200px',
								left: '50%',
                                height: '600px',
                                width: '1100px',
								color: 'rgb(0, 0, 0)',
								fontFamily: 'Montserrat',
								fontSize: '20px',
								fontWeight: '500',
								justifyContent: 'left',
								textAlign: 'left',
								borderRadius: '40px',
								backgroundColor: 'rgb(13, 207, 240)',
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
