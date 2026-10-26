# Copilot instructions

## Build, run, and validate

This is a Python desktop application; there is no separate build step or configured linter.

- Install dependencies: `python -m pip install -r requirements.txt`
- Launch the Tkinter app: `python app.py`
- Train and save the default model: `python train_model.py`
- Run the repository's combined implementation smoke checks: `python test_implementation.py`
- Run the standalone prediction example: `python predict.py`

`test_implementation.py` is a script, not a pytest/unittest suite; it checks imports, loads the saved model, exercises the decision path and prediction methods, and verifies GUI files. There are no individually selectable test cases or configured lint commands.

## Architecture

- `app.py` creates the Tkinter root and controller state. `gui/main_window.py` constructs the pages once and switches between them with `tkraise()`; pages receive the controller and call `on_show_page()` when activated.
- The diagnosis flow is `gui/input_page.py` -> `predict.py` -> the serialized model at `model/model_c45.joblib`. The latest input and result are stored in the controller's `shared_data["last_prediction"]`; `gui/result_page.py` displays them and `gui/visualization_page.py` uses them to highlight the decision path.
- `utils/c45.py` implements the numeric C4.5 decision tree and its prediction, probability, and decision-path APIs. Gain-ratio and threshold calculations live in the neighboring `utils/` modules. Scikit-learn is used for data splitting and evaluation, not as the decision-tree implementation.
- `utils/data_loader.py` reads `dataset/dataset.csv`. `gui/dataset_page.py` appends new labeled rows and can invoke `train_model.py`. Model training and pruning parameters are configured in scripts, not through a GUI page. Training writes the model and evaluation metrics under `model/`.
- `config.py` centralizes the project-root-relative dataset, model, and output paths. Use these constants rather than relying on the process working directory.

## Repository-specific conventions

- The dataset is semicolon-delimited. Its columns are `No`, eight numeric SMART features, and `Status`; `No` is a row identifier, not a model input. Class labels are `Normal` and `Rusak`.
- Keep the eight feature names and their order consistent wherever model data is assembled, especially between training, prediction, and GUI input. Training normalizes numeric values (including decimal commas) before fitting.
- The default model artifact is a joblib-serialized `C45Tree`. Training commands overwrite model artifacts and metrics in `model/`; retrain intentionally after changing the dataset or training parameters before evaluating predictions.
- GUI pages follow the `tk.Frame` page pattern: accept `parent_container` and `controller`, use controller methods for navigation/shared diagnosis state, and refresh page content in `on_show_page()` when it depends on current state.
- User-facing UI text and domain documentation are primarily in Indonesian; keep new labels and messages consistent with that language.
