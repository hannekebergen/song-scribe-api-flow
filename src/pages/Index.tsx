
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { MusicIcon, UsersIcon, FileTextIcon, BarChartIcon } from '@/components/icons/IconComponents';
import { Link } from 'react-router-dom';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            JouwSong
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Ontdek de toekomst van muziek met onze AI-gedreven songwriting platform. 
            Transformeer ideeën in prachtige liedjes met geavanceerde kunstmatige intelligentie.
          </p>
          <div className="space-x-4">
            <Button asChild size="lg" className="bg-blue-600 hover:bg-blue-700">
              <Link to="/dashboard">
                <BarChartIcon className="h-5 w-5 mr-2" />
                Dashboard
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to="/orders">
                <FileTextIcon className="h-5 w-5 mr-2" />
                Bestellingen
              </Link>
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MusicIcon className="h-6 w-6 text-blue-600" />
                AI Songwriting
              </CardTitle>
              <CardDescription>
                Geavanceerde AI-algoritmen creëren unieke liedjes op basis van jouw input
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Onze intelligente systemen analyseren je wensen en maken gepersonaliseerde songteksten die perfect aansluiten bij je verhaal.
              </p>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UsersIcon className="h-6 w-6 text-green-600" />
                Persoonlijk & Uniek
              </CardTitle>
              <CardDescription>
                Elk lied wordt speciaal voor jou gemaakt met persoonlijke details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Voeg persoonlijke verhalen, herinneringen en emoties toe om een lied te creëren dat echt van jou is.
              </p>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileTextIcon className="h-6 w-6 text-purple-600" />
                Eenvoudig Proces
              </CardTitle>
              <CardDescription>
                Van idee tot lied in enkele stappen
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Vertel ons over je wensen, kies je stijl, en laat onze AI de magie gebeuren. Binnen minuten heb je jouw unieke lied.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-12 text-white">
          <h2 className="text-3xl font-bold mb-4">Klaar om je verhaal te vertellen?</h2>
          <p className="text-xl mb-8 opacity-90">
            Begin vandaag nog met het maken van jouw gepersonaliseerde lied
          </p>
          <Button asChild size="lg" variant="secondary" className="bg-white text-blue-600 hover:bg-gray-100">
            <Link to="/dashboard">
              Start Nu
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
