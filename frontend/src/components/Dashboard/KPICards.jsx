import {useEffect,useState} from "react";

import api from "../../services/api";

import KPICard from "./KPICard";

export default function KPICards(){

const [kpi,setKpi]=useState({});

useEffect(()=>{

api.get("/dashboard/kpis")

.then(res=>setKpi(res.data));

},[]);

return(

<div className="kpi-grid">

<KPICard

title="Total Complaints"

value={kpi.total_complaints}

/>

<KPICard

title="Products"

value={kpi.products}

/>

<KPICard

title="Companies"

value={kpi.companies}

/>

<KPICard

title="States"

value={kpi.states}

/>

<KPICard

title="Avg Narrative"

value={kpi.average_length}

/>

</div>

);

}