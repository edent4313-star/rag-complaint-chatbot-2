import Layout from "../components/Layout/Layout";

import KPICards from "../components/Dashboard/KPICards";

import TrendChart from "../components/Dashboard/TrendChart";

import ProductChart from "../components/Dashboard/ProductChart";

import IssueChart from "../components/Dashboard/IssueChart";

import CompanyTable from "../components/Dashboard/CompanyTable";

export default function Dashboard(){

return(

<Layout>

<KPICards/>

<div className="grid">

<TrendChart/>

<ProductChart/>

<IssueChart/>

<CompanyTable/>

</div>

</Layout>

);

}