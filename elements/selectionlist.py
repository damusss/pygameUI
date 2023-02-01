import pygame
from .. import constants,global_input
from ..elements.container import UIScrollableContainer
from ..elements.scrollbar import UIVerticalScrollbar
from ..elements.button import UIButton

class UISelectionList(UIScrollableContainer):
    def __init__(self,relative_rect,ui_manager,starting_items_list=[],enable_multi_selection=False,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],inner_ids={
        "scrollbar":constants.DEFAULT_SETTINGS["default_element_id"],
        "elementprefix":constants.DEFAULT_SETTINGS["default_element_id"]
    }):
        super().__init__(relative_rect,ui_manager,container,True,visible,id,False,"selectionlist")
        
        self._element_prefix = inner_ids["elementprefix"]
        self._magic_number = self._settings["magic_numbers"]["selectionlist"]
        self._last_rebuild = global_input.GlobalInput.ticks
        self._items_list = starting_items_list
        self._enable_multi_selection = enable_multi_selection
        s = UIVerticalScrollbar(pygame.Rect(self.relative_rect.w-self._magic_number,0,self._magic_number,self.relative_rect.h),self.ui_manager,self,id=inner_ids["scrollbar"],_name="selectionlistscrollbar")
        self.set_vertical_scrollbar(s)
        self.on_rebuild(True,True)
        
    def get_selection(self):
        if not self._enable_multi_selection:
            for el in self._elements_right:
                if el is not self._vertical_scrollbar:
                    if el._is_clicking:
                        return el.get_text()
            return None
        raise Exception("Cannot get a single selection in 'UISelectionList' if 'enable_multi_selection' is True")
    
    def get_multi_selection(self):
        if self._enable_multi_selection:
            found = []
            for el in self._elements_right:
                if el is not self._vertical_scrollbar:
                    if el._is_clicking:
                        found.append(el.get_text())
            return found
        else:
            raise Exception("Cannot get multiple selections in 'UISelectionList' if 'enable_multi_selection' is False")
        
    def set_item_list(self,item_list):
        self._items_list = item_list
        self.on_rebuild(True,True)
        
    def _on_btn_select(self,btn):
        if not self._enable_multi_selection:
            old = None
            for el in self._elements_right:
                if (not el._is_scrollbar) and (not (el is btn)):
                    if el._is_clicking:
                        el._is_clicking = False
                        old = el
            pygame.event.post(pygame.event.Event(constants.SELECTION_CHANGED,{
                "old_selection":old.get_text() if old != None else None,
                "new_selection":btn.get_text(),
                "element_ID":self._ID,
                "element_object":self
            }))
        else:
            pygame.event.post(pygame.event.Event(constants.SELECTION_ADDED,{
                "selection":btn.get_text(),
                "element_ID":self._ID,
                "element_object":self
            }))
                    
    def _on_btn_deselect(self,btn):
        if self._enable_multi_selection:
            pygame.event.post(pygame.event.Event(constants.SELECTION_REMOVED,{
                "selection":btn.get_text(),
                "element_ID":self._ID,
                "element_object":self
            }))
        
    def on_rebuild(self,force=False,elements_changed=False):
        if (global_input.GlobalInput.ticks-self._last_rebuild > 10) or force:
            self._last_rebuild = global_input.GlobalInput.ticks
            if self._vertical_scrollbar:
                self._vertical_scrollbar.change_dimensions(self._vertical_scrollbar._magic_number,self.relative_rect.h)
                self._vertical_scrollbar.relative_rect.topright = (self.relative_rect.w,0)
                self._vertical_scrollbar.refresh_position()
                if elements_changed:
                    els = self._elements_right.copy()
                    for el in els:
                        if el is not self._vertical_scrollbar:
                            el.destroy()
                    i = 0
                    for item in self._items_list:
                        rect = pygame.Rect(0,self._magic_number*i,self.relative_rect.w-self._vertical_scrollbar._magic_number,self._magic_number)
                        btn = UIButton(rect,self.ui_manager,self,str(item),True,id=self._element_prefix+str(i),_name="selectionlistbutton")
                        btn._press_callback = self._on_btn_select
                        btn._release_callback = self._on_btn_deselect
                        btn._shape_renderer.oe = False
                        i+=1
                else:
                    for el in self._elements_right:
                        if el is not self._vertical_scrollbar:
                            el.change_dimensions(self.relative_rect.w-self._magic_number,self._magic_number)