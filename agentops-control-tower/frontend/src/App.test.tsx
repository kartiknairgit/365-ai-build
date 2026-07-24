import "@testing-library/jest-dom/vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("states the safe product purpose", () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/about"]}>
          <App />
        </MemoryRouter>
      </QueryClientProvider>,
    );
    expect(
      screen.getByRole("heading", { name: "About this prototype" }),
    ).toBeVisible();
    expect(screen.getByText(/does not execute agents or tools/i)).toBeVisible();
    expect(screen.getByRole("navigation", { name: "Primary" })).toBeVisible();
  });
});
