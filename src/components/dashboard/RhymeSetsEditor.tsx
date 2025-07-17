import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { EditIcon, XIcon, PlusIcon, TrashIcon, SaveIcon } from '@/components/icons/IconComponents';
import { ThemaRhymeSet, CreateRhymeSetRequest, UpdateRhymeSetRequest } from '@/services/themaApi';
import { themaApi } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';

interface RhymeSetsEditorProps {
  themaId: number;
  rhymeSets: ThemaRhymeSet[];
  isEditing: boolean;
  onToggleEdit: () => void;
  onRhymeSetsChange: () => void;
}

const RhymeSetsEditor: React.FC<RhymeSetsEditorProps> = ({ 
  themaId, 
  rhymeSets, 
  isEditing, 
  onToggleEdit,
  onRhymeSetsChange 
}) => {
  const [editingRhymeSet, setEditingRhymeSet] = useState<ThemaRhymeSet | null>(null);
  const [isAddingNew, setIsAddingNew] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [formData, setFormData] = useState<CreateRhymeSetRequest>({
    thema_id: themaId,
    rhyme_pattern: 'AABB',
    rhyme_pairs: [['', '']],
    difficulty_level: 'medium'
  });
  const { toast } = useToast();

  const handleToggleEdit = () => {
    if (isEditing) {
      toast({
        title: "Bewerkingsmodus uitgezet",
        description: "Je kunt nu rijmwoorden bekijken zonder te bewerken"
      });
    } else {
      toast({
        title: "Bewerkingsmodus ingeschakeld",
        description: "Je kunt nu rijmwoorden bewerken, toevoegen en verwijderen"
      });
    }
    onToggleEdit();
  };

  const openAddDialog = () => {
    setFormData({
      thema_id: themaId,
      rhyme_pattern: 'AABB',
      rhyme_pairs: [['', '']],
      difficulty_level: 'medium'
    });
    setIsAddingNew(true);
    setIsDialogOpen(true);
  };

  const openEditDialog = (rhymeSet: ThemaRhymeSet) => {
    setEditingRhymeSet(rhymeSet);
    setFormData({
      thema_id: themaId,
      rhyme_pattern: rhymeSet.rhyme_pattern,
      rhyme_pairs: [...rhymeSet.rhyme_pairs],
      difficulty_level: rhymeSet.difficulty_level
    });
    setIsAddingNew(false);
    setIsDialogOpen(true);
  };

  const closeDialog = () => {
    setIsDialogOpen(false);
    setEditingRhymeSet(null);
    setIsAddingNew(false);
  };

  const handleAddPair = () => {
    setFormData(prev => ({
      ...prev,
      rhyme_pairs: [...prev.rhyme_pairs, ['', '']]
    }));
  };

  const handleRemovePair = (index: number) => {
    setFormData(prev => ({
      ...prev,
      rhyme_pairs: prev.rhyme_pairs.filter((_, i) => i !== index)
    }));
  };

  const handlePairChange = (pairIndex: number, wordIndex: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      rhyme_pairs: prev.rhyme_pairs.map((pair, i) => 
        i === pairIndex 
          ? pair.map((word, j) => j === wordIndex ? value : word)
          : pair
      )
    }));
  };

  const handleSubmit = async () => {
    try {
      // Filter out empty pairs and validate
      const filteredPairs = formData.rhyme_pairs
        .map(pair => pair.map(word => word.trim()))
        .filter(pair => pair[0] !== '' && pair[1] !== '');
      
      if (filteredPairs.length < 1) {
        toast({
          title: "Fout",
          description: "Voeg minimaal 1 rijmend paar toe",
          variant: "destructive"
        });
        return;
      }

      const submitData = {
        ...formData,
        rhyme_pairs: filteredPairs
      };

      if (isAddingNew) {
        await themaApi.createRhymeSet(submitData);
        toast({
          title: "Rijmset toegevoegd",
          description: `Nieuwe rijmwoorden set met patroon ${submitData.rhyme_pattern} toegevoegd`
        });
      } else {
        await themaApi.updateRhymeSet(editingRhymeSet!.id, submitData);
        toast({
          title: "Rijmset bijgewerkt",
          description: `Rijmwoorden set met patroon ${submitData.rhyme_pattern} bijgewerkt`
        });
      }

      closeDialog();
      onRhymeSetsChange();
    } catch (error) {
      toast({
        title: "Fout",
        description: error instanceof Error ? error.message : "Er is een fout opgetreden",
        variant: "destructive"
      });
    }
  };

  const handleDelete = async (rhymeSet: ThemaRhymeSet) => {
    if (!confirm(`Weet je zeker dat je de rijmwoorden set "${rhymeSet.rhyme_pattern}" wilt verwijderen?`)) {
      return;
    }

    try {
      await themaApi.deleteRhymeSet(rhymeSet.id);
      toast({
        title: "Rijmset verwijderd",
        description: `Rijmwoorden set met patroon ${rhymeSet.rhyme_pattern} verwijderd`
      });
      onRhymeSetsChange();
    } catch (error) {
      toast({
        title: "Fout",
        description: error instanceof Error ? error.message : "Er is een fout opgetreden",
        variant: "destructive"
      });
    }
  };

  const getDifficultyColor = (level: string) => {
    switch (level) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyLabel = (level: string) => {
    switch (level) {
      case 'easy': return 'Makkelijk';
      case 'medium': return 'Gemiddeld';
      case 'hard': return 'Moeilijk';
      default: return level;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with edit toggle and summary */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h3 className="text-lg font-semibold text-gray-900">Rijmwoorden Sets</h3>
          <div className="flex gap-2">
            <Badge variant="outline" className="text-xs">
              {rhymeSets.length} sets
            </Badge>
            <Badge variant="outline" className="text-xs">
              {rhymeSets.reduce((total, set) => total + set.rhyme_pairs.length, 0)} paren
            </Badge>
          </div>
        </div>
        <div className="flex gap-2">
          {isEditing && (
            <Button
              variant="outline"
              size="sm"
              onClick={openAddDialog}
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Nieuwe Set
            </Button>
          )}
          <Button
            variant={isEditing ? "destructive" : "default"}
            size="sm"
            onClick={handleToggleEdit}
          >
            {isEditing ? (
              <>
                <XIcon className="h-4 w-4 mr-2" />
                Stoppen met bewerken
              </>
            ) : (
              <>
                <EditIcon className="h-4 w-4 mr-2" />
                Bewerken
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Edit mode notice */}
      {isEditing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-2 text-blue-800">
            <EditIcon className="h-4 w-4" />
            <span className="text-sm font-medium">Bewerkingsmodus actief</span>
          </div>
          <p className="text-sm text-blue-700 mt-1">
            Je kunt nu rijmwoorden sets bewerken, toevoegen en verwijderen. Klik op de bewerk-knop naast elke set om het te wijzigen.
          </p>
        </div>
      )}

      {/* Rhyme sets list */}
      <div className="space-y-4">
        {rhymeSets.length === 0 ? (
          <Card className="bg-gray-50">
            <CardContent className="p-8 text-center">
              <div className="text-gray-500 mb-4">
                <EditIcon className="h-8 w-8 mx-auto mb-2" />
                <p className="text-sm">Geen rijmwoorden sets gevonden voor dit thema</p>
              </div>
              {isEditing && (
                <p className="text-xs text-gray-400">
                  Klik op "Nieuwe Set" om rijmwoorden toe te voegen
                </p>
              )}
            </CardContent>
          </Card>
        ) : (
          rhymeSets.map((rhymeSet) => (
            <Card key={rhymeSet.id} className="border-l-4 border-l-blue-500">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <CardTitle className="text-lg font-semibold">
                      Patroon: {rhymeSet.rhyme_pattern}
                    </CardTitle>
                    <Badge className={getDifficultyColor(rhymeSet.difficulty_level)}>
                      {getDifficultyLabel(rhymeSet.difficulty_level)}
                    </Badge>
                  </div>
                  {isEditing && (
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => openEditDialog(rhymeSet)}
                      >
                        <EditIcon className="h-4 w-4 mr-2" />
                        Bewerken
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(rhymeSet)}
                      >
                        <TrashIcon className="h-4 w-4 mr-2" />
                        Verwijderen
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {rhymeSet.rhyme_pairs.map((pair, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <Badge variant="secondary" className="text-sm">
                        {pair[0]}
                      </Badge>
                      <span className="text-gray-400">↔</span>
                      <Badge variant="secondary" className="text-sm">
                        {pair[1]}
                      </Badge>
                    </div>
                  ))}
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  {rhymeSet.rhyme_pairs.length} rijmende paren • Toegevoegd op {new Date(rhymeSet.created_at).toLocaleDateString('nl-NL')}
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {isAddingNew ? 'Nieuwe Rijmwoorden Set' : 'Rijmwoorden Set Bewerken'}
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Rhyme Pattern */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="rhyme-pattern">Rijm Patroon</Label>
                <Select 
                  value={formData.rhyme_pattern} 
                  onValueChange={(value) => setFormData(prev => ({ ...prev, rhyme_pattern: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Kies patroon" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="AABB">AABB (Koppelrijm)</SelectItem>
                    <SelectItem value="ABAB">ABAB (Kruisrijm)</SelectItem>
                    <SelectItem value="ABBA">ABBA (Omarmend rijm)</SelectItem>
                    <SelectItem value="AAAA">AAAA (Monorijm)</SelectItem>
                    <SelectItem value="ABCB">ABCB (Ballade)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="difficulty">Moeilijkheidsgraad</Label>
                <Select 
                  value={formData.difficulty_level} 
                  onValueChange={(value) => setFormData(prev => ({ ...prev, difficulty_level: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Kies niveau" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="easy">Makkelijk</SelectItem>
                    <SelectItem value="medium">Gemiddeld</SelectItem>
                    <SelectItem value="hard">Moeilijk</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Rhyme Pairs */}
            <div>
              <Label>Rijmende Paren</Label>
              <div className="space-y-3 mt-2">
                {formData.rhyme_pairs.map((pair, pairIndex) => (
                  <div key={pairIndex} className="flex items-center gap-2">
                    <Input
                      value={pair[0]}
                      onChange={(e) => handlePairChange(pairIndex, 0, e.target.value)}
                      placeholder="Eerste woord"
                      className="flex-1"
                    />
                    <span className="text-gray-400 font-bold">↔</span>
                    <Input
                      value={pair[1]}
                      onChange={(e) => handlePairChange(pairIndex, 1, e.target.value)}
                      placeholder="Rijmend woord"
                      className="flex-1"
                    />
                    {formData.rhyme_pairs.length > 1 && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleRemovePair(pairIndex)}
                      >
                        <XIcon className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleAddPair}
                  className="w-full"
                >
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Rijmend Paar Toevoegen
                </Button>
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-2 pt-4">
              <Button variant="outline" onClick={closeDialog}>
                Annuleren
              </Button>
              <Button onClick={handleSubmit}>
                <SaveIcon className="h-4 w-4 mr-2" />
                {isAddingNew ? 'Toevoegen' : 'Opslaan'}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Summary footer */}
      <div className="border-t pt-4">
        <div className="flex justify-between items-center text-sm text-gray-600">
          <span>
            Laatste wijziging: {new Date().toLocaleString('nl-NL')}
          </span>
          <span>
            {rhymeSets.length} rijmwoorden sets met {rhymeSets.reduce((total, set) => total + set.rhyme_pairs.length, 0)} paren
          </span>
        </div>
      </div>
    </div>
  );
};

export default RhymeSetsEditor; 