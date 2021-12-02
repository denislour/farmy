import React from "react";
import { Layout, LandingPage } from "../components";
import { EuiText } from "@elastic/eui";

export default function App() {
  return (
    <Layout>
      <EuiText>
        <LandingPage />
      </EuiText>
    </Layout>
  );
}
