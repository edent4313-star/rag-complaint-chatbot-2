import { NavLink } from "react-router-dom";

import {
    MdDashboard,
    MdAnalytics,
    MdChat,
    MdAssessment,
    MdSettings
} from "react-icons/md";

import "./Layout.css";

export default function Sidebar() {

    return (

        <aside className="sidebar">

            <h2>

                Complaint AI

            </h2>

            <NavLink to="/">

                <MdDashboard />

                Dashboard

            </NavLink>

            <NavLink to="/analytics">

                <MdAnalytics />

                Analytics

            </NavLink>

            <NavLink to="/chat">

                <MdChat />

                AI Chat

            </NavLink>

            <NavLink to="/evaluation">

                <MdAssessment />

                Evaluation

            </NavLink>

            <NavLink to="/settings">

                <MdSettings />

                Settings

            </NavLink>

        </aside>

    );

}