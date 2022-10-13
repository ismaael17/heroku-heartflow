import React, { Component, useState } from 'react'
import './DirectorHomePage_Deliveries.css'
import ImgAsset from '../public'
import { Link } from 'react-router-dom'
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { Button, rgbToHex } from "@material-ui/core";
import AuthService from "../Services/auth.service";
import { useEffect } from 'react';
import VolunteersService from "../Services/volunteers.service";


const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'amount', headerName: 'No. of Coupons', width: 150 },
    { field: 'serial_letter', headerName: 'Serial Letter', width: 150 },
    { field: 'range_from', headerName: 'Range from', width: 150 },
    { field: 'range_to', headerName: 'Range To', width: 200 },
    { field: 'date', headerName: 'Date', width: 300 },
    { field: 'comments', headerName: 'Comment', width: 300 },
    { field: 'paymentMethod', headerName: 'Payment Method', width: 300 },
    { field: 'flag', headerName: 'Flagged', width: 300 },
    { field: 'paid', headerName: 'Paid', width: 300 },
    { field: 'companyName', headerName: 'Company ID', width: 300 },
    { field: 'volunteer', headerName: 'Volunteer ID', width: 300 },

];

export default function DirectorHomePage_Deliveries() {

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
        VolunteersService.getDeliveries(
            localStorage.getItem("userToken"),
            "Director"
        ).then(response => {
            setDataGridRows(dataGridRows => [])
            for (let i = 0; i < response.data['length']; i++) {
                setDataGridRows(dataGridRows => [...dataGridRows, { id: response.data[i]['id'],  companyName :response.data[i]['company'], serial_letter: response.data[i]['serial_letter'], range_from: response.data[i]['range_from'], range_to: response.data[i]['range_to'], paymentMethod: response.data[i]['payment_method'], amount: response.data[i]['amount'], paid:response.data[i]['paid'], date: response.data[i]['date'], comments: response.data[i]['comments'], flag: response.data[i]['flag'], volunteer: response.data[i]['volunteer']}])
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
                <div className='DirectorHomePage_Deliveries'>

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
                            pageSize={5}
                            rowsPerPageOptions={[5]}
                            sx={{
                                top: '200px',
								left: '20%',
                                height: '600px',
                                width: '1600px',
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
