import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ChatInput from "../components/Chat/ChatInput";

describe("ChatInput", () => {
    let onSend;

    beforeEach(() => {
        onSend = vi.fn();
    });

    it("renders the textarea", () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        expect(screen.getByRole("textbox")).toBeInTheDocument();
    });

    it("renders the send button", () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        expect(screen.getByRole("button", { name: /send/i })).toBeInTheDocument();
    });

    it("send button is disabled when input is empty", () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        expect(screen.getByRole("button", { name: /send/i })).toBeDisabled();
    });

    it("send button becomes enabled when user types", async () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        await userEvent.type(screen.getByRole("textbox"), "hello");
        expect(screen.getByRole("button", { name: /send/i })).toBeEnabled();
    });

    it("calls onSend with trimmed text on button click", async () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        await userEvent.type(screen.getByRole("textbox"), "  test question  ");
        fireEvent.click(screen.getByRole("button", { name: /send/i }));
        expect(onSend).toHaveBeenCalledWith("test question");
    });

    it("clears the textarea after submission", async () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        const textarea = screen.getByRole("textbox");
        await userEvent.type(textarea, "some question");
        fireEvent.click(screen.getByRole("button", { name: /send/i }));
        expect(textarea.value).toBe("");
    });

    it("calls onSend when Enter is pressed", async () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        const textarea = screen.getByRole("textbox");
        await userEvent.type(textarea, "Enter question");
        fireEvent.keyDown(textarea, { key: "Enter", shiftKey: false });
        expect(onSend).toHaveBeenCalledWith("Enter question");
    });

    it("does NOT call onSend when Shift+Enter is pressed", async () => {
        render(<ChatInput onSend={onSend} disabled={false} />);
        const textarea = screen.getByRole("textbox");
        await userEvent.type(textarea, "line one");
        fireEvent.keyDown(textarea, { key: "Enter", shiftKey: true });
        expect(onSend).not.toHaveBeenCalled();
    });

    it("disables textarea and button when disabled prop is true", () => {
        render(<ChatInput onSend={onSend} disabled={true} />);
        expect(screen.getByRole("textbox")).toBeDisabled();
        expect(screen.getByRole("button", { name: /send/i })).toBeDisabled();
    });

    it("does not call onSend when disabled and Enter pressed", async () => {
        render(<ChatInput onSend={onSend} disabled={true} />);
        const textarea = screen.getByRole("textbox");
        fireEvent.keyDown(textarea, { key: "Enter", shiftKey: false });
        expect(onSend).not.toHaveBeenCalled();
    });
});
