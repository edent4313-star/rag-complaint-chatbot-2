import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import KPICard from "../components/Dashboard/KPICard";

describe("KPICard", () => {
    it("renders without crashing", () => {
        render(<KPICard title="Total Complaints" value={1234} />);
    });

    it("displays the title", () => {
        render(<KPICard title="Total Complaints" value={1234} />);
        expect(screen.getByText("Total Complaints")).toBeInTheDocument();
    });

    it("displays a numeric value", () => {
        render(<KPICard title="Products" value={42} />);
        expect(screen.getByText("42")).toBeInTheDocument();
    });

    it("displays a string value", () => {
        render(<KPICard title="Rate" value="98.5%" />);
        expect(screen.getByText("98.5%")).toBeInTheDocument();
    });

    it("renders when value is 0", () => {
        render(<KPICard title="Issues" value={0} />);
        expect(screen.getByText("0")).toBeInTheDocument();
    });

    it("renders when value is undefined (loading state)", () => {
        // Should not throw; value may be undefined while data loads
        render(<KPICard title="Companies" value={undefined} />);
        expect(screen.getByText("Companies")).toBeInTheDocument();
    });

    it("renders an optional icon", () => {
        const Icon = () => <svg data-testid="icon" />;
        render(<KPICard title="States" value={50} icon={<Icon />} />);
        expect(screen.getByTestId("icon")).toBeInTheDocument();
    });

    it("renders correctly without icon prop", () => {
        render(<KPICard title="No icon" value={10} />);
        expect(screen.getByText("No icon")).toBeInTheDocument();
    });

    it("applies the kpi-card class to the root element", () => {
        const { container } = render(<KPICard title="Test" value={1} />);
        expect(container.firstChild).toHaveClass("kpi-card");
    });
});
