import os
from flask import Flask, render_template, jsonify, request
import threading
import time

app = Flask(__name__)

# Конфигурация
ANIMATIONS_FOLDER = os.path.join('static', 'animations')
DEFAULT_TIMER_MINUTES = 5

class AnimationPlayer:
    def __init__(self):
        self.animations = []
        self.current_index = 0
        self.timer_enabled = False
        self.timer_minutes = DEFAULT_TIMER_MINUTES
        self.timer_thread = None
        self.load_animations()
    
    def load_animations(self):
        """Загружает список анимаций из папки"""
        self.animations = []
        if os.path.exists(ANIMATIONS_FOLDER):
            for file in os.listdir(ANIMATIONS_FOLDER):
                if file.endswith('.html'):
                    self.animations.append(file)
        else:
            os.makedirs(ANIMATIONS_FOLDER, exist_ok=True)
    
    def get_current_animation(self):
        """Возвращает текущую анимацию"""
        if not self.animations:
            return None
        return self.animations[self.current_index]
    
    def next_animation(self):
        """Переключает на следующую анимацию"""
        if not self.animations:
            return None
        self.current_index = (self.current_index + 1) % len(self.animations)
        return self.get_current_animation()
    
    def previous_animation(self):
        """Переключает на предыдущую анимацию"""
        if not self.animations:
            return None
        self.current_index = (self.current_index - 1) % len(self.animations)
        return self.get_current_animation()
    
    def set_animation(self, animation_name):
        """Устанавливает конкретную анимацию по имени"""
        if animation_name in self.animations:
            self.current_index = self.animations.index(animation_name)
            return True
        return False
    
    def start_timer(self):
        """Запускает таймер автоматического переключения"""
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
    
    def _timer_loop(self):
        """Цикл автоматического переключения"""
        while self.timer_enabled:
            time.sleep(self.timer_minutes * 60)
            if self.timer_enabled:
                self.next_animation()

player = AnimationPlayer()

@app.route('/')
def index():
    """Основная страница плеера"""
    return render_template('player.html')

@app.route('/current-animation', methods=['GET'])
def get_current_animation():
    """Получение текущей анимации"""
    return jsonify({
        'success': True,
        'animation': player.get_current_animation(),
        'index': player.current_index,
        'total': len(player.animations)
    })

@app.route('/list-animations', methods=['GET'])
def list_animations():
    """Получение списка всех анимаций"""
    return jsonify({
        'success': True,
        'animations': player.animations,
        'current_index': player.current_index
    })

@app.route('/set-animation', methods=['POST'])
def set_animation():
    """Установка конкретной анимации по имени"""
    data = request.get_json()
    animation_name = data.get('animation')
    if animation_name and player.set_animation(animation_name):
        return jsonify({
            'success': True,
            'animation': player.get_current_animation()
        })
    return jsonify({
        'success': False,
        'error': 'Animation not found'
    }), 404

@app.route('/next', methods=['GET'])
def next_animation():
    """Переключение на следующую анимацию"""
    new_anim = player.next_animation()
    return jsonify({
        'success': True,
        'animation': new_anim,
        'index': player.current_index
    })

@app.route('/previous', methods=['GET'])
def previous_animation():
    """Переключение на предыдущую анимацию"""
    new_anim = player.previous_animation()
    return jsonify({
        'success': True,
        'animation': new_anim,
        'index': player.current_index
    })

@app.route('/enable-timer', methods=['GET'])
def enable_timer():
    """Включение таймера автоматического переключения"""
    player.timer_enabled = True
    player.start_timer()
    return jsonify({
        'success': True,
        'timer_enabled': True,
        'timer_minutes': player.timer_minutes
    })

@app.route('/disable-timer', methods=['GET'])
def disable_timer():
    """Выключение таймера автоматического переключения"""
    player.timer_enabled = False
    return jsonify({
        'success': True,
        'timer_enabled': False
    })

@app.route('/set-timer', methods=['GET'])
def set_timer():
    """Установка интервала таймера в минутах"""
    minutes = request.args.get('minutes', default=DEFAULT_TIMER_MINUTES, type=int)
    if minutes > 0:
        player.timer_minutes = minutes
        return jsonify({
            'success': True,
            'minutes': player.timer_minutes
        })
    return jsonify({
        'success': False,
        'error': "Invalid timer value"
    }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)