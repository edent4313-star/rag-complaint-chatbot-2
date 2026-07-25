import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import SourceCard from "../components/Chat/SourceCard";

const BASE_SOURCE = {
    document: "The customer reported an unauthorized charge on their account.",
    product:  "Credit card",
    company:  "Bank A",
    issue:    "Billing error",
    state:    "CA",
    score:    0.87,
};

describe("SourceCard", () => {
    it("renders without crashing", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
    });

    it("shows the source index number (1-based)", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText("#1")).toBeInTheDocument();
    });

    it("shows a different index for index=2", () => {
        render(<SourceCard source={BASE_SOURCE} index={2} />);
        expect(screen.getByText("#3")).toBeInTheDocument();
    });

    it("shows the relevance score as a percentage", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText(/87\.0% match/i)).toBeInTheDocument();
    });

    it("shows the document preview text", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText(/unauthorized charge/i)).toBeInTheDocument();
    });

    it("truncates long documents with an ellipsis", () => {
        const longSource = {
            ...BASE_SOURCE,
            document: "A".repeat(300),
        };
        render(<SourceCard source={longSource} index={0} />);
        expect(screen.getByText(/A+…/)).toBeInTheDocument();
    });

    it("renders the product tag", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText("Credit card")).toBeInTheDocument();
    });

    it("renders the company tag", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText("Bank A")).toBeInTheDocument();
    });

    it("renders the issue tag", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText("Billing error")).toBeInTheDocument();
    });

    it("renders the state tag", () => {
        render(<SourceCard source={BASE_SOURCE} index={0} />);
        expect(screen.getByText("CA")).toBeInTheDocument();
    });

    it("handles missing score gracefully (no crash)", () => {
        const noScore = { ...BASE_SOURCE, score: null };
        render(<SourceCard source={noScore} index={0} />);
        expect(screen.getByText("#1")).toBeInTheDocument();
    });

    it("handles missing optional fields gracefully", () => {
        const minimal = { document: "Some complaint text.", score: 0.5 };
        render(<SourceCard source={minimal} index={0} />);
        expect(screen.getByText(/Some complaint text/i)).toBeInTheDocument();
    });

    it("shows fallback text when document is missing", () => {
        const noDoc = { ...BASE_SOURCE, document: null };
        render(<SourceCard source={noDoc} index={0} />);
        expect(screen.getByText(/no narrative available/i)).toBeInTheDocument();
    });
});
