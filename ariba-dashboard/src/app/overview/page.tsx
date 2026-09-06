/*
  Overview page for Ariba Security Platform Dashboard
*/

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useTable } from "@/hooks/use-table";
import { AlertCard } from "@/components/alert-card";

export default function OverviewPage() {
  // Mock data for alerts
  const alerts = [
    { id: "1", title: "SQL Injection Attempt", severity: "critical", time: "2 min ago" },
    { id: "2", title: "Brute Force Login", severity: "high", time: "15 min ago" },
    { id: "3", title": "Port Scan Detected", severity: "medium", time: "1 hour ago" },
  ];

  return (
    <div className="main-content">
      <h1 className="mb-6 text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {/* Critical Alerts Card */}
        <AlertCard>
          <CardHeader>
            <CardTitle>Critical Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <Badge className="badge critical">3 active</Badge>
          </CardContent>
        </AlertCard>
        
        {/* High Severity Card */}
        <AlertCard>
          <CardHeader>
            <CardTitle>High Severity</CardTitle>
          </CardHeader>
          <CardContent>
            <Badge className="badge high">2 active</Badge>
          </CardContent>
        </AlertCard>
        
        {/* Medium Severity Card */}
        <AlertCard>
          <CardHeader>
            <CardTitle>Medium Severity</CardTitle>
          </CardHeader>
          <CardContent>
            <Badge className="badge medium">5 active</Badge>
          </CardContent>
        </AlertCard>
      </div>
      
      {/* Recent Events Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Events */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Events</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-text">No recent events</p>
          </CardContent>
        </Card>
        
        {/* Threat Hunting */}
        <Card>
          <CardHeader>
            <CardTitle>Threat Hunting</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-text">Start a hunting query</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}