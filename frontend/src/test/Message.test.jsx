import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Message from "../components/Chat/Message";

describe("Message", () => {
    describe("user role", () => {
        it("renders the message content", () => {
            render(<Message role="user" content="Hello there" />);
            expect(screen.getByText("Hello there")).toBeInTheDocument();
        });

        it("applies the user CSS modifier class", () => {
            const { container } = render(<Message role="user" content="Hi" />);
            expect(container.firstChild).toHaveClass("message--user");
        });

        it("does NOT apply the assistant class for user messages", () => {
            const { container } = render(<Message role="user" content="Hi" />);
            expect(container.firstChild).not.toHaveClass("message--assistant");
        });
    });

    describe("assistant role", () => {
        it("renders the assistant message content", () => {
            render(<Message role="assistant" content="I can help you." />);
            expect(screen.getByText("I can help you.")).toBeInTheDocument();
        });

        it("applies the assistant CSS modifier class", () => {
            const { container } = render(<Message role="assistant" content="Hi" />);
            expect(container.firstChild).toHaveClass("message--assistant");
        });

        it("does NOT apply the user class for assistant messages", () => {
            const { container } = render(<Message role="assistant" content="Hi" />);
            expect(container.firstChild).not.toHaveClass("message--user");
        });
    });

    describe("multi-line content", () => {
        it("renders each line as a separate paragraph", () => {
            render(<Message role="assistant" content={"Line one\nLine two\nLine three"} />);
            expect(screen.getByText("Line one")).toBeInTheDocument();
            expect(screen.getByText("Line two")).toBeInTheDocument();
            expect(screen.getByText("Line three")).toBeInTheDocument();
        });
    });

    describe("avatar", () => {
        it("renders an avatar element", () => {
            const { container } = render(<Message role="user" content="test" />);
            expect(container.querySelector(".message__avatar")).toBeInTheDocument();
        });
    });

    describe("bubble", () => {
        it("renders a bubble element", () => {
            const { container } = render(<Message role="user" content="test" />);
            expect(container.querySelector(".message__bubble")).toBeInTheDocument();
        });
    });
});
