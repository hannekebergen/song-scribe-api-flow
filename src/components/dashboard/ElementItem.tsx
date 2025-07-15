import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { EditIcon, TrashIcon, CheckIcon, XIcon } from '@/components/icons/IconComponents';
import { ThemaElement, themaApi } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';

interface ElementItemProps {
  element: ThemaElement;
  isEditing: boolean;
  onDelete: () => void;
  onUpdate: () => void;
}

const ElementItem: React.FC<ElementItemProps> = ({ 
  element, 
  isEditing, 
  onDelete, 
  onUpdate 
}) => {
  const [isEditingContent, setIsEditingContent] = useState(false);
  const [editContent, setEditContent] = useState(element.content);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSaveEdit = async () => {
    if (editContent.trim() === element.content) {
      setIsEditingContent(false);
      return;
    }

    if (!editContent.trim()) {
      toast({
        title: "Fout",
        description: "Content mag niet leeg zijn",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      await themaApi.updateElement(element.id, {
        content: editContent.trim()
      });
      
      setIsEditingContent(false);
      onUpdate();
      
      toast({
        title: "Succes",
        description: "Element succesvol bijgewerkt"
      });
    } catch (error) {
      console.error('Error updating element:', error);
      setEditContent(element.content); // Reset on error
      toast({
        title: "Fout",
        description: "Kon element niet bijwerken",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditContent(element.content);
    setIsEditingContent(false);
  };

  const handleDelete = async () => {
    if (!confirm('Weet je zeker dat je dit element wilt verwijderen?')) return;
    
    setIsLoading(true);
    try {
      await themaApi.deleteElement(element.id);
      onDelete();
      
      toast({
        title: "Succes",
        description: "Element succesvol verwijderd"
      });
    } catch (error) {
      console.error('Error deleting element:', error);
      toast({
        title: "Fout",
        description: "Kon element niet verwijderen",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-between p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors">
      <div className="flex-1">
        {isEditingContent ? (
          <div className="flex gap-2">
            <Input
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSaveEdit();
                if (e.key === 'Escape') handleCancelEdit();
              }}
              className="text-sm"
              autoFocus
              disabled={isLoading}
            />
            <Button 
              size="sm" 
              variant="outline" 
              onClick={handleSaveEdit}
              disabled={isLoading}
            >
              <CheckIcon className="h-3 w-3" />
            </Button>
            <Button 
              size="sm" 
              variant="outline" 
              onClick={handleCancelEdit}
              disabled={isLoading}
            >
              <XIcon className="h-3 w-3" />
            </Button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <span className="text-sm">{element.content}</span>
            {element.usage_context && (
              <Badge variant="secondary" className="text-xs">
                {element.usage_context}
              </Badge>
            )}
            {element.weight > 1 && (
              <Badge variant="outline" className="text-xs">
                weight: {element.weight}
              </Badge>
            )}
          </div>
        )}
      </div>

      {isEditing && !isEditingContent && (
        <div className="flex gap-1">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setIsEditingContent(true)}
            className="text-blue-600 hover:text-blue-800"
            disabled={isLoading}
          >
            <EditIcon className="h-3 w-3" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={handleDelete}
            className="text-red-600 hover:text-red-800"
            disabled={isLoading}
          >
            <TrashIcon className="h-3 w-3" />
          </Button>
        </div>
      )}
    </div>
  );
};

export default ElementItem; 