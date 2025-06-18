
import React, { forwardRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { EditIcon, SaveIcon, RotateIcon, CheckIcon } from '@/components/icons/IconComponents';

interface SongEditorProps {
  editedSongtext: string;
  setEditedSongtext: (text: string) => void;
  hasChanges: boolean;
  saving: boolean;
  originalSongtext: string;
  onSave: () => void;
  onReset: () => void;
}

const SongEditor = forwardRef<HTMLTextAreaElement, SongEditorProps>(({
  editedSongtext,
  setEditedSongtext,
  hasChanges,
  saving,
  originalSongtext,
  onSave,
  onReset
}, ref) => {
  return (
    <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center justify-between text-gray-800">
          <div className="flex items-center gap-2">
            <EditIcon className="h-5 w-5 text-purple-600" />
            Songtekst Editor
          </div>
          {hasChanges && (
            <Badge variant="outline" className="text-orange-600 border-orange-200 bg-orange-50 animate-pulse">
              Niet opgeslagen
            </Badge>
          )}
        </CardTitle>
        <Separator />
      </CardHeader>
      <CardContent className="space-y-6">
        <Textarea
          ref={ref}
          value={editedSongtext}
          onChange={(e) => setEditedSongtext(e.target.value)}
          placeholder="Songtekst..."
          className="min-h-[500px] font-mono text-sm leading-relaxed border-gray-200 focus:border-purple-500 focus:ring-purple-500 resize-none"
        />
        
        <div className="flex flex-col sm:flex-row gap-3">
          <Button 
            onClick={onSave}
            disabled={!hasChanges || saving}
            className="flex-1 bg-green-600 hover:bg-green-700 text-white"
          >
            <SaveIcon className="h-4 w-4 mr-2" />
            {saving ? 'Opslaan...' : 'Opslaan'}
          </Button>
          
          {hasChanges && (
            <Button 
              variant="outline"
              onClick={onReset}
              className="border-gray-200 hover:bg-gray-50"
            >
              <RotateIcon className="h-4 w-4 mr-2" />
              Reset
            </Button>
          )}
        </div>

        {originalSongtext && originalSongtext.length > 0 && (
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center gap-2 mb-2">
              <CheckIcon className="h-4 w-4 text-blue-600" />
              <span className="text-sm font-medium text-blue-800">
                Status: Songtekst beschikbaar
              </span>
            </div>
            <p className="text-sm text-blue-700">
              De songtekst is {originalSongtext.split('\n').length} regels lang en bevat {originalSongtext.length} karakters.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
});

SongEditor.displayName = "SongEditor";

export default SongEditor;
