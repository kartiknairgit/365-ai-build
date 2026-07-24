import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("states the safe product purpose", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: "AgentOps Control Tower" }),
    ).toBeVisible();
    expect(
      screen.getByText(/without executing agents or tools/i),
    ).toBeVisible();
  });
});
