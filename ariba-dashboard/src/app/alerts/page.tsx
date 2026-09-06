/*
  Alerts page for Ariba Security Platform Dashboard
*/

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Table, TableHeader, TableBody, TableRow, TableCell, TableHead } from "@/components/ui/table";
import { useTable } from "@/hooks/use-table";
import { AlertCard } from "@/components/alert-card";

export default function AlertsPage() {
  const { data: alerts, isLoading } = useTable({
    endpoint: "/api/v1/alerts",
    columns: ["id", "title", "severity", "status", "createdAt", "actions"],
  });

  return (
    <div className="main-content">
      <h1 className="mb-6 text-3xl font-bold">Alerts</h1>
      
      {isLoading && <p>Loading alerts...</p>}
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {/* Summary cards - same structure as overview */}
        <div className="space-y-2">
          <AlertCard>
            <CardHeader><CardTitle>Critical</CardTitle></CardHeader>
            <CardContent><Badge className="badge critical">3</Badge></CardContent>
          </AlertCard>
          <AlertCard>
            <CardHeader><CardTitle>High</CardTitle></CardHeader>
            <CardContent><Badge className="badge high">2</Badge></CardContent>
          </AlertCard>
        </div>
        <AlertCard>
          <CardHeader><CardTitle>Medium</CardTitle></CardHeader>
          <CardContent><Badge className="badge medium">5</Badge></CardContent>
        </AlertCard>
        <AlertCard>
          <CardHeader><CardTitle>Low</CardTitle></CardHeader>
          <CardContent><Badge className="badge low">1</Badge></CardContent>
        </AlertCard>
      </div>
      
      {/* Alerts table */}
      <Card>
        <CardHeader>
          <CardTitle>Alert Details</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p>Loading...</p>
          ) : alerts.length === 0 ? (
            <p className="text-muted-text">No alerts found</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Severity</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHeader>
              <TableBody>
                {alerts.map((alert) => (
                  <TableRow key={alert.id}>
                    <TableCell>{alert.id}</TableCell>
                    <TableCell>{alert.title}</TableCell>
                    <TableCell>
                      <Badge className={`badge ${alert.severity.toLowerCase()}`}>
                        {alert.severity}
                      </Badge>
                    </TableCell>
                    <TableCell>{alert.status}</TableCell>
                    <TableCell>{alert.createdAt}</TableCell>
                    <TableCell>
                      <Button size="sm" variant="outline">Investigate</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}