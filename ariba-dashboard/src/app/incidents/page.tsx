/*
  Incidents page for Ariba Security Platform Dashboard
*/

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Table, TableHeader, TableBody, TableRow, TableHead } from "@/components/ui/table";
import { useTable } from "@/hooks/use-table";
import { Badge } from "@/components/ui/badge";

export default function IncidentsPage() {
  const { data: incidents, isLoading } = useTable({
    endpoint: "/api/v1/incidents",
    columns: ["id", "title", "severity", "status", "owner", "createdAt", "actions"],
  });

  return (
    <div className="main-content">
      <h1 className="mb-6 text-3xl font-bold">Incidents</h1>
      
      {isLoading && <p>Loading incidents...</p>}
      
      {/* Incidents table */}
      <Card>
        <CardHeader>
          <CardTitle>Incident Details</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p>Loading...</p>
          ) : incidents.length === 0 ? (
            <p className="text-muted-text">No incidents found</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Severity</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Owner</TableCell>
                  <TableCell>Created</TableCell>
                </TableRow>
              </TableHeader>
              <TableBody>
                {incidents.map((incident) => (
                  <TableRow key={incident.id}>
                    <TableCell>{incident.id}</TableCell>
                    <TableCell>{incident.title}</TableCell>
                    <TableCell>
                      <Badge className={`badge ${incident.severity.toLowerCase()}`}>
                        {incident.severity}
                      </Badge>
                    </TableCell>
                    <TableCell>{incident.status}</TableCell>
                    <TableCell>{incident.owner || "Unassigned"}</TableCell>
                    <TableCell>{incident.createdAt}</TableCell>
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