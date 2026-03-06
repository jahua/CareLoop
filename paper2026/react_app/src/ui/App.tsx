import { Button, Card } from "../components";
import { Calendar } from "../components/Calendar";

export function App() {
  return (
    <div style={{ padding: 24, fontFamily: "ui-sans-serif, system-ui" }}>
      <h1 style={{ marginTop: 0 }}>Hello React + TypeScript + Vite</h1>
      <Card title="Sample Card">
        <p>This is a simple reusable card component.</p>
        <div style={{ display: "flex", gap: 8 }}>
          <Button onClick={() => alert("Primary clicked")}>Primary</Button>
          <Button variant="secondary" onClick={() => alert("Secondary clicked")}>Secondary</Button>
        </div>
      </Card>
      <div style={{ marginTop: 24 }}>
        <Calendar />
      </div>
    </div>
  );
}


