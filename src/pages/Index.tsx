
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Music, Users, FileText, BarChart3 } from 'lucide-react';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            JouwSong.nl
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Beheer je gepersonaliseerde songtekstorders met ons moderne dashboard
          </p>
          
          <Button asChild size="lg" className="text-lg px-8 py-6">
            <Link to="/dashboard">
              <BarChart3 className="mr-2 h-5 w-5" />
              Open Dashboard
            </Link>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <Music className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <CardTitle>Songtekst Beheer</CardTitle>
              <CardDescription>
                Beheer alle orders en gegenereerde songteksten op één plek
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Order overzicht en filtering</li>
                <li>• Real-time status updates</li>
                <li>• Zoeken op voornaam</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <FileText className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <CardTitle>Editor & Downloads</CardTitle>
              <CardDescription>
                Edit songteksten en download in verschillende formaten
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Ingebouwde tekst editor</li>
                <li>• JSON en TXT downloads</li>
                <li>• Auto-save functionaliteit</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <Users className="h-12 w-12 text-purple-600 mx-auto mb-4" />
              <CardTitle>API Integratie</CardTitle>
              <CardDescription>
                Klaar voor koppeling met jouw Python backend
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• REST API endpoints</li>
                <li>• Webhook ondersteuning</li>
                <li>• Mock data voor development</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        <div className="mt-16 text-center">
          <Card className="max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-2xl">Klaar voor Productie</CardTitle>
              <CardDescription>
                Dit dashboard is gebouwd met moderne technologieën en klaar voor deployment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-semibold">React 18</div>
                  <div className="text-gray-600">Modern framework</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-semibold">TypeScript</div>
                  <div className="text-gray-600">Type safety</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-semibold">Tailwind CSS</div>
                  <div className="text-gray-600">Responsive design</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-semibold">shadcn/ui</div>
                  <div className="text-gray-600">Modern components</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;
