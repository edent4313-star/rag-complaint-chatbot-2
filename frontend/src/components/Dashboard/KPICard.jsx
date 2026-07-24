export default function KPICard({

title,

value,

icon,

color

}){

return(

<div className="kpi-card">

<div>

<h4>{title}</h4>

<h2>{value}</h2>

</div>

<div>

{icon}

</div>

</div>

);

}